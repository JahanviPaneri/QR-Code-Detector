from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import os
from model import predict_photo

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify({'message': 'Photo Detector API is running'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if image is present in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Read the image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Validate image format
        if image.format not in ['PNG', 'JPEG', 'JPG', 'GIF']:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Call model prediction
        result = predict_photo(image)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f'Error processing image: {str(e)}')
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

