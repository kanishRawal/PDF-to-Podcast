import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [audioUrl, setAudioUrl] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/pdf') {
        setError('Please select a valid PDF file.');
        setFile(null);
      } else {
        setError('');
        setFile(selectedFile);
        setAudioUrl('');
      }
    }
  };

  const handleGenerate = async () => {
    if (!file) return;
    
    setLoading(true);
    setError('');
    setAudioUrl('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Assuming backend runs on 8000
      const response = await fetch('http://localhost:8000/generate-podcast', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = 'Failed to generate podcast.';
        try {
          const errData = await response.json();
          errorMsg = errData.detail || errorMsg;
        } catch(e) {
          errorMsg = response.statusText || errorMsg;
        }
        throw new Error(errorMsg);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🎙️ PDF to Podcast</h1>
        <p>Turn any PDF document into an engaging two-host podcast episode.</p>
      </header>

      <main className="main-content">
        <div className="upload-section">
          <label className="file-label">
            <input 
              type="file" 
              accept=".pdf" 
              onChange={handleFileChange}
              disabled={loading}
              className="file-input"
            />
            <span className="file-custom">{file ? file.name : "Choose a PDF file..."}</span>
          </label>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button 
          className="generate-btn"
          onClick={handleGenerate}
          disabled={!file || loading}
        >
          {loading ? "Generating your podcast, this may take a minute..." : "Generate Podcast"}
        </button>

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Our AI hosts are reading your document and recording their lines. Hang tight!</p>
          </div>
        )}

        {audioUrl && (
          <div className="result-section">
            <h2>Your Podcast is Ready!</h2>
            <audio controls src={audioUrl} className="audio-player">
              Your browser does not support the audio element.
            </audio>
            <a href={audioUrl} download={`${file?.name.replace('.pdf', '')}_podcast.mp3`} className="download-btn">
              Download MP3
            </a>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
