# Photo Detector Backend

Flask API for photo detection using ML models.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The API will run on http://localhost:5000

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /predict` - Upload image and get prediction

## Usage

POST to `/predict` with multipart/form-data containing an 'image' field.

