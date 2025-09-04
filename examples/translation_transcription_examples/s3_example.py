#!/usr/bin/env python3
"""
S3 Presigned URL Example
This script demonstrates how to use S3 presigned URLs with the transcription and translation API.
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
    """Example using S3 presigned URLs"""
    
    # Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://34.212.19.243:8000')
    API_KEY = os.getenv('API_KEY', None)
    AUDIO_S3_URL = os.getenv('AUDIO_S3_URL', None)
    SRT_S3_URL = os.getenv('SRT_S3_URL', None)  # For translation example
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'downloads')
    TRANSLATION_LANGUAGES = os.getenv('TRANSLATION_LANGUAGES', 'es,fr,de').split(',')
    JOB_TIMEOUT = int(os.getenv('JOB_TIMEOUT', '30'))
    
    print("🌐 S3 Presigned URL Example")
    print("=" * 50)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Audio S3 URL: {AUDIO_S3_URL}")
    print(f"SRT S3 URL: {SRT_S3_URL}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Translation Languages: {', '.join(TRANSLATION_LANGUAGES)}")
    print()
    
    if not AUDIO_S3_URL:
        print("❌ AUDIO_S3_URL environment variable not set.")
        print("   Set it to your S3 presigned URL for an audio file.")
        print("   Example: export AUDIO_S3_URL='https://your-bucket.s3.amazonaws.com/audio.mp3?presigned-params'")
        sys.exit(1)
    
    # Initialize client
    client = TranscribeTranslateClient(API_BASE_URL, API_KEY)
    
    # Check API health
    if not client.health_check():
        print("❌ API is not healthy. Exiting.")
        sys.exit(1)
    
    print()
    
    try:
        # Example 1: Transcription using S3 URL
        print("🎵 Example 1: Transcription using S3 URL")
        transcription_job_id = client.start_transcription(s3_presigned_url=AUDIO_S3_URL)
        print()
        
        # Wait for transcription to complete
        if not client.wait_for_job_completion(transcription_job_id, "transcription", JOB_TIMEOUT):
            print("❌ Transcription failed. Exiting.")
            sys.exit(1)
        print()
        
        # Download transcription results
        transcription_files = client.download_job_results(transcription_job_id, OUTPUT_DIR)
        print()
        
        # Example 2: Translation using S3 URL (if provided)
        if SRT_S3_URL:
            print("🌐 Example 2: Translation using S3 URL")
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
            print(f"   Transcription Job ID: {transcription_job_id}")
            print(f"   Translation Job ID: {translation_job_id}")
            print(f"   Transcription Files: {len(transcription_files)}")
            print(f"   Translation Files: {len(translation_files)}")
        else:
            print("📋 Summary:")
            print(f"   Transcription Job ID: {transcription_job_id}")
            print(f"   Transcription Files: {len(transcription_files)}")
            print("   (Set SRT_S3_URL environment variable to test translation with S3)")
        
        print(f"   Output Directory: {os.path.abspath(OUTPUT_DIR)}")
        print()
        print("🎉 S3 examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
