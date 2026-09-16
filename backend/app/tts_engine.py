import os
import edge_tts
import tempfile

async def synthesize_line(text: str, voice: str, output_path: str):
    """
    Synthesizes a single line of text into an audio file.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

async def generate_audio_segments(script: list[dict]) -> list[str]:
    """
    Generates audio segments for the entire script.
    Returns a list of file paths to the generated temporary audio files.
    """
    # Voices:
    # A natural sounding male and female voice for US English.
    voice_a = "en-US-AriaNeural" # Female
    voice_b = "en-US-GuyNeural"  # Male

    segment_paths = []
    
    for i, line in enumerate(script):
        speaker = line.get("speaker")
        text = line.get("text")
        
        voice = voice_a if speaker == "A" else voice_b
        
        # Create a temp file path
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd) # Close the file descriptor, edge_tts will open it to write
        
        await synthesize_line(text, voice, path)
        segment_paths.append(path)
        
    return segment_paths
