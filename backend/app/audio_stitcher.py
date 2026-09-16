from pydub import AudioSegment
import os
def stitch_audio_segments(segment_paths: list[str], output_path: str):
    """
    Stitches multiple audio segments together with a small silence gap.
    """
    if not segment_paths:
        raise ValueError("No audio segments to stitch.")
        
    # 500ms silence between speakers
    silence_gap = AudioSegment.silent(duration=500) 
    
    combined = AudioSegment.empty()
    
    for i, path in enumerate(segment_paths):
        segment = AudioSegment.from_file(path)
        if i > 0:
            combined += silence_gap
        combined += segment
        
    combined.export(output_path, format="mp3")
    
    # Cleanup temp files
    for path in segment_paths:
        try:
            os.remove(path)
        except Exception:
            pass
