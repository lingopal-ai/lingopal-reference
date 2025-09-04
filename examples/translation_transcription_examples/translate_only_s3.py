#!/usr/bin/env python3
"""
Translation Only with S3 Example
This script demonstrates how to use S3 presigned URLs for translation only (skipping transcription).
"""

import os
import sys
from transcribe_and_translate import TranscribeTranslateClient

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

def main():
    """Example using S3 presigned URL for translation only"""
    
    # Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://34.212.19.243:8000')
    API_KEY = os.getenv('API_KEY', None)
    SRT_S3_URL = os.getenv('SRT_S3_URL', None)
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'downloads')
    TRANSLATION_LANGUAGES = os.getenv('TRANSLATION_LANGUAGES', 'es,fr,de').split(',')
    JOB_TIMEOUT = int(os.getenv('JOB_TIMEOUT', '30'))
    
    print("🌐 Translation Only with S3 Example")
    print("=" * 50)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"SRT S3 URL: {SRT_S3_URL}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Translation Languages: {', '.join(TRANSLATION_LANGUAGES)}")
    print()
    
    if not SRT_S3_URL:
        print("❌ SRT_S3_URL environment variable not set.")
        print("   Set it to your S3 presigned URL for an SRT file.")
        print("   Example: export SRT_S3_URL='https://your-bucket.s3.amazonaws.com/subtitles.srt?presigned-params'")
        sys.exit(1)
    
    # Initialize client
    client = TranscribeTranslateClient(API_BASE_URL, API_KEY)
    
    # Check API health
    if not client.health_check():
        print("❌ API is not healthy. Exiting.")
        sys.exit(1)
    
    print()
    
    try:
        # Start translation using S3 URL
        print("🌐 Starting translation using S3 URL")
        translation_job_id = client.start_translation(s3_presigned_url=SRT_S3_URL, target_languages=TRANSLATION_LANGUAGES)
        print()
        
        # Wait for translation to complete
        if not client.wait_for_job_completion(translation_job_id, "translation", JOB_TIMEOUT):
            print("❌ Translation failed. Exiting.")
            sys.exit(1)
        print()
        
        # Download translation results
        translation_files = client.download_job_results(translation_job_id, OUTPUT_DIR)
        print()
        
        # Summary
        print("📋 Summary:")
        print(f"   Translation Job ID: {translation_job_id}")
        print(f"   Translation Files: {len(translation_files)}")
        print(f"   Output Directory: {os.path.abspath(OUTPUT_DIR)}")
        print()
        print("🎉 Translation with S3 completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
