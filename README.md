# PDF to Podcast

Turn any PDF document into an engaging two-host podcast episode using AI.

This application uses:
- **FastAPI** for the backend
- **PyMuPDF** for text extraction
- **Google Gemini API** for script generation
- **edge-tts** for voice synthesis
- **pydub** for audio stitching
- **React + Vite** for the frontend

## Prerequisites

1. Python 3.10+
2. Node.js 18+
3. `ffmpeg` installed and available on your system PATH. (Required by `pydub`)

## How to Run

Follow these steps exactly in your terminal to start the application.

### 1. Backend Setup

Open a terminal and navigate to the project root, then run:

```powershell
# Create and activate virtual environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit the .env file and add your GEMINI_API_KEY
copy .env.example .env

# Start the backend server (runs on http://localhost:8000)
uvicorn app.main:app --reload
```

### 2. Frontend Setup

Open a **new, separate terminal**, navigate to the project root, then run:

```powershell
cd frontend

# Install dependencies (if you haven't already)
npm install

# Start the frontend dev server (typically runs on http://localhost:5173)
npm run dev
```

### 3. Usage

1. Open your browser to the frontend URL (usually `http://localhost:5173`).
2. Upload a PDF file.
3. Click "Generate Podcast" and wait for the AI to process and synthesize the audio.
4. Listen to the final audio and download it!
