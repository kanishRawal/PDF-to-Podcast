import os
import json
from google import genai
from google.genai import types

def generate_podcast_script(text: str) -> list[dict]:
    """
    Generates a two-host podcast script from the given text using Gemini API.
    Returns a list of dictionaries with 'speaker' and 'text' keys.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not set or invalid in environment variables.")

    client = genai.Client(api_key=api_key)
    
    prompt = f"""You are an expert podcast producer. Create a natural, engaging two-host podcast conversation based on the following text.
Host A should explain the material in an accessible way, and Host B should act as the curious co-host who asks questions, pushes back gently, and adds reactions.
Return your response ONLY as valid JSON matching this schema:
[
  {{ "speaker": "A", "text": "..." }},
  {{ "speaker": "B", "text": "..." }}
]

Source text:
{text}
"""
    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            break # Success
        except Exception as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to generate script from Gemini API after {max_retries} attempts: {e}")
            print(f"Attempt {attempt+1} failed with {e}. Retrying...")
            time.sleep(2)

    try:
        script = json.loads(response.text)
        if not isinstance(script, list):
            raise ValueError("Parsed JSON is not a list.")
        for line in script:
            if "speaker" not in line or "text" not in line:
                raise ValueError("Missing 'speaker' or 'text' in script line.")
        return script
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse Gemini response as JSON: {response.text}")
    except Exception as e:
        raise ValueError(f"Invalid script format received: {e}")
