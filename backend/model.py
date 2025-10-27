import numpy as np
from PIL import Image
import random

def predict_photo(image):
    """
    Predict if a photo is real or fake.
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: {
            'prediction': 'real' or 'fake',
            'confidence': confidence percentage
        }
    """
    try:
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image for processing
        image = image.resize((224, 224))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Simple heuristic-based approach (replace with actual ML model)
        # This is a placeholder that analyzes basic image properties
        
        # Extract features
        avg_brightness = np.mean(img_array)
        std_dev = np.std(img_array)
        
        # Edge detection simulation (LAPLACIAN-like)
        gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
        laplacian = np.abs(np.diff(gray, n=1))
        edge_score = np.mean(laplacian)
        
        # Color variance
        color_variance = np.var(img_array.reshape(-1, 3), axis=0)
        color_score = np.mean(color_variance)
        
        # Fake detection heuristics (can be improved with actual ML model)
        # Lower brightness and edge scores might indicate fake/manipulated images
        # This is a simplified approach
        
        brightness_score = avg_brightness / 255.0
        edge_normalized = edge_score / 100.0
        color_normalized = color_score / 1000.0
        
        # Calculate fake probability (placeholder logic)
        # Adjust these thresholds based on your actual model
        fake_probability = 0.3  # Base probability
        
        # Increase fake probability if certain conditions are met
        if brightness_score < 0.2:
            fake_probability += 0.2
        if edge_normalized < 0.05:
            fake_probability += 0.2
        if color_normalized < 0.01:
            fake_probability += 0.1
        
        # Add some randomness for demo purposes
        # In production, this would be replaced with actual model inference
        fake_probability += random.uniform(-0.1, 0.1)
        fake_probability = max(0.0, min(1.0, fake_probability))
        
        # Determine prediction
        if fake_probability > 0.5:
            prediction = 'fake'
            confidence = int(fake_probability * 100)
        else:
            prediction = 'real'
            confidence = int((1 - fake_probability) * 100)
        
        return {
            'prediction': prediction,
            'confidence': confidence
        }
        
    except Exception as e:
        print(f'Error in model prediction: {str(e)}')
        # Return a default prediction on error
        return {
            'prediction': 'real',
            'confidence': 50
        }

