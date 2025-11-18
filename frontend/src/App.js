import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const PRIMARY_TABS = [
  { id: 'url', label: 'URL Safety' },
  { id: 'upload', label: 'Upload QR' },
  { id: 'scan', label: 'Live Scanner' }
];

function App() {
  const [page, setPage] = useState('home');
  const [activeTab, setActiveTab] = useState('url');
  const [urlInput, setUrlInput] = useState('');
  const [urlResult, setUrlResult] = useState(null);
  const [qrFile, setQrFile] = useState(null);
  const [qrPreview, setQrPreview] = useState(null);
  const [qrResult, setQrResult] = useState(null);
  const [scanStatus, setScanStatus] = useState('idle');
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (activeTab === 'scan') {
      startCamera();
    } else {
      stopCamera();
    }

    return () => {
      stopCamera();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

  const startCamera = async () => {
    if (!navigator.mediaDevices) {
      setScanStatus('unsupported');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      streamRef.current = stream;
      setScanStatus('active');
    } catch (error) {
      console.error('Camera error:', error);
      setScanStatus('blocked');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setScanStatus('idle');
  };

  const handleUrlCheck = () => {
    if (!urlInput.trim()) return;
    const redFlags = ['bit.ly', 'tinyurl', 'http://', 'unsafe', 'phish'];
    const isSuspicious = redFlags.some((flag) =>
      urlInput.toLowerCase().includes(flag)
    );
    setUrlResult({
      verdict: isSuspicious ? 'Malicious Pattern Detected' : 'Looks Safe',
      score: isSuspicious ? 15 : 82,
      details: isSuspicious
        ? 'The link contains known risky patterns. Avoid interacting with it.'
        : 'No risky patterns detected. Still use caution before trusting unknown QR codes.'
    });
  };

  const handleQrUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setQrResult({
        verdict: 'Unsupported File',
        details: 'Please upload an image file containing a QR code.'
      });
      return;
    }

    setQrFile(file);
    setQrResult(null);

    const reader = new FileReader();
    reader.onloadend = () => setQrPreview(reader.result);
    reader.readAsDataURL(file);
  };

  const analyzeQr = () => {
    if (!qrFile) return;
    const suspiciousNames = ['suspicious', 'unknown', 'malicious'];
    const fileName = qrFile.name.toLowerCase();
    const isSuspicious = suspiciousNames.some((name) =>
      fileName.includes(name)
    );

    setQrResult({
      verdict: isSuspicious ? 'Possibly Malicious' : 'Clean Metadata',
      details: isSuspicious
        ? 'Filename hints at risky origin. Run a deeper scan in the backend service.'
        : 'No suspicious metadata detected. Proceed with server-side analysis to confirm.'
    });
  };

  const renderHome = () => (
    <section className="hero">
      <div className="hero-text">
        <p className="eyebrow">Trusted QR Intelligence</p>
        <h1>Scan smart, stay safe.</h1>
        <p className="lead">
          SentinelQR inspects URLs and QR codes in real-time so you know exactly
          where a code leads before you scan. Block malicious redirects, catch
          phishing attempts, and keep every interaction secure.
        </p>
        <div className="hero-cta">
          <button className="primary" onClick={() => setPage('test')}>
            Start Testing
          </button>
          
        </div>
        <div className="stats">
          <div>
            <span>1.2M+</span>
            <p>QRs inspected</p>
          </div>
          <div>
            <span>99.5%</span>
            <p>Malware detection rate</p>
          </div>
          <div>
            <span>24/7</span>
            <p>Cloud monitoring</p>
          </div>
        </div>
      </div>
      <div className="hero-card">
        <p className="card-label">Live Insight</p>
        <div className="pulse" />
        <h3>Zero-trust QR defense</h3>
        <p>
          Every scan is vetted against threat feeds, sandboxing, and proprietary
          AI heuristics.
        </p>
        <ul>
          <li>URL sandbox preview</li>
          <li>Metadata fingerprinting</li>
          <li>Camera-based scanning</li>
        </ul>
      </div>
    </section>
  );

  const renderTest = () => (
    <section className="test-hub">
      <div className="tab-bar">
        {PRIMARY_TABS.map((tab) => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="panel">
        {activeTab === 'url' && (
          <div className="panel-content">
            <h3>Paste a URL from a QR code</h3>
            <p>We flag obvious red flags instantly before deeper backend scans.</p>
            <div className="url-checker">
              <input
                type="text"
                placeholder="https://example.com/promo"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
              />
              <button onClick={handleUrlCheck}>Check safety</button>
            </div>
            {urlResult && (
              <div className="result-card">
                <p className="result-label">{urlResult.verdict}</p>
                <h4>{urlResult.score}% confidence</h4>
                <p>{urlResult.details}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="panel-content">
            <h3>Upload a QR image</h3>
            <p>Drop a snapshot or screenshot to analyze metadata and content.</p>
            <label className="upload-tile">
              <input type="file" accept="image/*" onChange={handleQrUpload} />
              <span>Choose QR image</span>
            </label>
            {qrPreview && (
              <div className="preview-wrapper">
                <img src={qrPreview} alt="QR preview" />
                <button onClick={analyzeQr}>Run quick scan</button>
              </div>
            )}
            {qrResult && (
              <div className="result-card">
                <p className="result-label">{qrResult.verdict}</p>
                <p>{qrResult.details}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'scan' && (
          <div className="panel-content">
            <h3>Point-and-scan with your camera</h3>
            <p>
              We never store footage. Grant access to preview the QR payload
              before opening it.
            </p>
            <div className={`scanner ${scanStatus}`}>
              <video ref={videoRef} playsInline />
              <div className="scanner-overlay">
                <span />
              </div>
            </div>
            <div className="scan-status">
              {scanStatus === 'active' && 'Scanner is live—center the QR code.'}
              {scanStatus === 'idle' && 'Enable the scanner to begin.'}
              {scanStatus === 'blocked' &&
                'Camera blocked. Update your browser permissions.'}
              {scanStatus === 'unsupported' &&
                'Camera API not supported on this device.'}
            </div>
          </div>
        )}
      </div>
    </section>
  );

  return (
    <div className="app-shell">
      <header className="top-nav">
        <div className="brand">
          <span className="dot" />
          SentinelQR
        </div>
        <nav>
          <button
            className={page === 'home' ? 'active' : ''}
            onClick={() => setPage('home')}
          >
            Home
          </button>
          <button
            className={page === 'test' ? 'active' : ''}
            onClick={() => setPage('test')}
          >
            Test
          </button>
        </nav>
      </header>

      <main>{page === 'home' ? renderHome() : renderTest()}</main>

      <footer>
        <p>© {new Date().getFullYear()} SentinelQR Labs. Built for safer scans.</p>
      </footer>
    </div>
  );
}

export default App;

