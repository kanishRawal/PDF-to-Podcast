from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import tempfile
import static_ffmpeg
static_ffmpeg.add_paths()

from app.pdf_extractor import extract_text_from_pdf
from app.script_generator import generate_podcast_script
from app.tts_engine import generate_audio_segments
from app.audio_stitcher import stitch_audio_segments

load_dotenv()

app = FastAPI(title="PDF to Podcast API")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@app.post("/generate-podcast")
async def generate_podcast(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # Read the file
        file_bytes = await file.read()
        
        # 1. Extract text
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(file_bytes)
        
        # 2. Generate script
        print("Generating podcast script with Gemini...")
        script = generate_podcast_script(text)
        
        # 3. Generate audio segments
        print("Generating audio segments using TTS...")
        segment_paths = await generate_audio_segments(script)
        
        # 4. Stitch audio segments
        print("Stitching audio segments...")
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        
        stitch_audio_segments(segment_paths, output_path)
        
        # Schedule cleanup of the final output file after it's sent
        background_tasks.add_task(remove_file, output_path)
        
        return FileResponse(
            path=output_path, 
            media_type="audio/mpeg", 
            filename="podcast.mp3"
        )
        
    except ValueError as e:
        print(f"Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

