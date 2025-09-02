import httpx
import json
import os
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Schedule a stream with Lingopal API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python schedule_stream.py --ingest_url "srt://your.server:7070" --scheduled_time "2024-01-15 10:00:00" --timezone "America/New_York"
  python schedule_stream.py --ingest_url "srt://stream.example.com:8080" --scheduled_time "2024-01-20 14:30:00" --timezone "Europe/London"
  python schedule_stream.py --ingest_url "srt://live.server:9090" --scheduled_time "2024-02-01 09:00:00" --timezone "Asia/Tokyo"
        """
    )
    
    parser.add_argument(
        "--ingest_url",
        required=True,
        help="The SRT ingest URL (e.g., 'srt://your.server:7070')"
    )
    
    parser.add_argument(
        "--scheduled_time",
        required=True,
        help="Scheduled start time in ISO 8601 format (e.g., '2024-01-15 10:00:00')"
    )
    
    parser.add_argument(
        "--timezone",
        required=True,
        help="Regional timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')"
    )
    
    return parser.parse_args()

# Get command line arguments
args = parse_arguments()

# Required environment variables
API_KEY = os.getenv("LINGOPAL_API_KEY")
API_URL = os.getenv("LINGOPAL_API_URL", "https://streaming.lingopal.ai/v1/scheduled_streams")

# Check required environment variables
if not API_KEY:
    raise ValueError("❌ Please set the LINGOPAL_API_KEY environment variable.")

# Payload for scheduling a stream
payload = {
    "ingest_url": args.ingest_url,
    "vocals_track": "0",
    "background_track": -1,
    "mix": "-9,-6",
    "enable_captions_708": False,
    "enable_captions_608": False,
    "dst_language": ["es"],
    "src_language": "en",
    "start_wowza": False,
    "use_contextual_translation": False,
    "lipsync": True,
    "channel_uuid": "string",
    "is_hls_stream": False,
    "use_reserved_resources": False,
    "stitching": False,
    "voice_cloning": True,
    "scheduled_time": args.scheduled_time,  
    "timezone": args.timezone
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
