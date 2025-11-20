from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import pandas as pd
import re
from urllib.parse import urlparse
from qr_decoder import decode_qr_bytes

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "model", "random_forest_model.pkl"
)

model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"[+] Model loaded from {MODEL_PATH}")
    else:
        print(f"[!] Model NOT found at: {MODEL_PATH}")
except Exception as e:
    print(f"[!] Error loading model: {e}")

# Feature columns used during training
FEATURE_COLUMNS = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_digits",
    "num_special_chars",
    "has_https",
    "num_subdirs",
    "num_params",
    "has_ip_address",
    "tld_length",
    "contains_suspicious_words",
]

def extract_features(url: str) -> dict:
    """Extract handcrafted URL features."""
    parsed = urlparse(str(url))
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": sum(c in "?=&%" for c in url),
        "has_https": 1 if url.lower().startswith("https") else 0,
        "num_subdirs": path.count("/"),
        "num_params": query.count("=") if query else 0,
        "has_ip_address": 1 if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 0,
    }

    tld_match = re.search(r"\.([a-z]+)(\/|$)", domain)
    features["tld_length"] = len(tld_match.group(1)) if tld_match else 0

    suspicious_words = [
        "login", "secure", "verify", "account",
        "update", "free", "bonus", "bank"
    ]
    features["contains_suspicious_words"] = (
        1 if any(w in url.lower() for w in suspicious_words) else 0
    )
    for key, value in features.items():
        print(key, value)
    print("--------------------------------")
    return features


class URLInput(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "API is running", "model_loaded": model is not None}


@app.post("/decode")
async def decode_qr(file: UploadFile = File(...)):
    """Decode QR code containing a URL."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        img_bytes = await file.read()
        decoded_url = decode_qr_bytes(img_bytes)

        if not decoded_url:
            raise HTTPException(status_code=400, detail="QR code not detected")

        return {"url": decoded_url.strip(), "message": "QR decoded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
def predict(data: URLInput):
    """Predict if URL is safe or malicious."""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    url = data.url.strip()
    print(url)
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    try:
        features = extract_features(url)
        df = pd.DataFrame([features])
        print(df)
        # add any missing columns
        for col in FEATURE_COLUMNS:
            if col not in df:
                df[col] = 0

        df = df[FEATURE_COLUMNS]
    
        pred = model.predict(df)
        pred = pred[0]
        print(pred)
        try:
            conf = float(max(model.predict_proba(df)[0]))
        except:
            conf = 0.5

        verdict = "safe" if pred == 1 else "malicious"

        return {
            "url": url,
            "prediction": int(pred),
            "verdict": verdict,
            "confidence": round(conf * 100, 2),
            "message": "Safe URL" if pred == 1 else "Malicious URL"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
