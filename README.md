# Photo Detector - Real or Fake

A web application that detects whether uploaded photos are real or fake using AI/ML techniques.

## 🚀 Features

- **Photo Upload**: Drag-and-drop or click to upload images
- **Real-time Detection**: Instantly determines if a photo is real or fake
- **Confidence Score**: Shows the confidence percentage of the prediction
- **Modern UI**: Beautiful, responsive interface with gradient designs

## 📁 Project Structure

```
QR-Code-Detector/
├── frontend/          # React frontend application
│   ├── src/
│   │   ├── App.js     # Main React component
│   │   ├── App.css    # Styling
│   │   └── index.js   # Entry point
│   └── package.json   # Dependencies
│
├── backend/           # Flask backend API
│   ├── app.py         # Flask application
│   ├── model.py       # Prediction logic
│   └── requirements.txt
│
└── README.md          # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will be running on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be running on `http://localhost:3000`

## 📖 Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click or drag an image to upload
3. Click "Analyze Photo" to get the prediction
4. View the result showing whether the photo is "Real" or "Fake" with confidence percentage

## 🧠 Model Details

The `model.py` file contains a placeholder prediction system using image analysis heuristics. You can integrate your own ML model by replacing the `predict_photo()` function.

Current features analyzed:
- Image brightness
- Edge detection
- Color variance
- Image quality metrics

To integrate a real ML model (like a trained CNN):
1. Load your trained model in `model.py`
2. Preprocess the image according to your model's requirements
3. Run inference and return the prediction

## 🔧 API Endpoints

### POST `/predict`
Upload an image for prediction.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `image` (file)

**Response:**
```json
{
  "prediction": "real",
  "confidence": 85
}
```

### GET `/health`
Check API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🛡️ Supported Image Formats

- PNG
- JPG/JPEG
- GIF

Maximum file size: 10MB

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📝 License

This project is open source and available for educational purposes.
