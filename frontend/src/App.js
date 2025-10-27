import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if file is an image
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        return;
      }
      setSelectedFile(file);
      setError(null);
      setResult(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
      setError(null);
    } catch (err) {
      console.error('Upload error:', err);
      setError('Failed to process image. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">🔍 Photo Detector</h1>
        <p className="subtitle">Upload a photo to detect if it's Real or Fake</p>

        <div className="upload-section">
          {!previewUrl ? (
            <div className="upload-area">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                id="fileInput"
                style={{ display: 'none' }}
              />
              <label htmlFor="fileInput" className="upload-label">
                <div className="upload-icon">📁</div>
                <p>Click to select an image</p>
                <span className="file-info">PNG, JPG, JPEG up to 10MB</span>
              </label>
            </div>
          ) : (
            <div className="preview-section">
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
                <div className="preview-overlay">
                  <button onClick={handleReset} className="reset-btn">
                    Change Image
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {selectedFile && !loading && !result && (
          <button onClick={handleUpload} className="submit-btn">
            Analyze Photo
          </button>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Analyzing your photo...</p>
          </div>
        )}

        {result && (
          <div className={`result-container ${result.prediction === 'real' ? 'real' : 'fake'}`}>
            <div className="result-icon">
              {result.prediction === 'real' ? '✓' : '✗'}
            </div>
            <h2 className="result-title">
              {result.prediction === 'real' ? 'Real Photo' : 'Fake Photo'}
            </h2>
            <p className="result-confidence">
              Confidence: {result.confidence}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

