import os
import requests
from dotenv import load_dotenv
from prompts.system_prompt import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

# Active, supported Gemini Flash models in priority order
CANDIDATE_FLASH_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
]


def get_api_key() -> str:
    """Retrieve GEMINI_API_KEY from environment variables."""
    return os.getenv("GEMINI_API_KEY", "").strip()


def organize_notes(raw_notes: str) -> str:
    """Organize unorganized notes using Google Gemini API.

    Sends notes and system instructions to Gemini and returns structured
    Markdown with topic clusters and bullet points.
    """
    api_key = get_api_key()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is missing or not configured. "
            "Please configure your API key in the .env file."
        )

    if not raw_notes or not raw_notes.strip():
        raise ValueError("Input notes cannot be empty. Please paste your notes first.")

    # 1. Attempt using google-genai SDK if available
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        for model_name in CANDIDATE_FLASH_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=raw_notes,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    ),
                )
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue
    except (ImportError, Exception):
        # Fall back to direct official REST API
        pass

    # 2. REST API fallback (official Google Generative Language API)
    headers = {"Content-Type": "application/json"}
    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Please organize the following unorganized notes into topic clusters with headings and bullet points:\n\n{raw_notes}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096,
        }
    }

    last_error_msg = None
    for model_name in CANDIDATE_FLASH_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
            elif resp.status_code == 404:
                continue
            elif resp.status_code == 400:
                err_data = resp.json().get("error", {})
                raise ValueError(f"API Request Error: {err_data.get('message', 'Invalid request')}")
            elif resp.status_code == 403:
                raise ValueError("API Key Error: Invalid or unauthorized Gemini API key.")
            elif resp.status_code == 429:
                raise ValueError("Quota Exceeded: You have hit the Gemini API rate limit. Please wait a moment.")
            else:
                last_error_msg = f"HTTP {resp.status_code}: {resp.text}"
        except requests.exceptions.Timeout:
            last_error_msg = f"Network Timeout with model {model_name}."
            continue
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Network Connection Error: Could not reach Google Gemini API.")
        except ValueError:
            raise

    raise RuntimeError(
        f"Unable to generate response from Gemini Flash models. {last_error_msg or 'Please check your connection and API key.'}"
    )
