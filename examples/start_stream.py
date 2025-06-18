import httpx
import json
import os

# Required environment variables
API_KEY = os.getenv("LINGOPAL_API_KEY")
INGEST_URL = os.getenv("LINGOPAL_INGEST_URL")
API_URL = os.getenv("LINGOPAL_API_URL", "https://streaming.lingopal.ai/v1/streams/start")

# Check required variables
if not API_KEY:
    raise ValueError("❌ Please set the LINGOPAL_API_KEY environment variable.")
if not INGEST_URL:
    raise ValueError("❌ Please set the LINGOPAL_INGEST_URL environment variable.")

# Payload
payload = {
    "ingest_url": INGEST_URL,
    "vocals_track": "0",
    "background_track": 1,
    "mix": "-9,-6",
    "enable_captions_708": True,
    "enable_captions_608": False,
    "src_language": "en",
    "dst_language": ["es"],
    "use_paraphrasing_transcription": True,
    "start_wowza": True,
    "is_hls_stream": False,
    "use_contextual_translation": False,
    "lipsync": False
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-API-Key": API_KEY
}

if __name__ == "__main__":
    response = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print("Non-JSON response:")
        print(response.text)
