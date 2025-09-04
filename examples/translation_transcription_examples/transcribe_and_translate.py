#!/usr/bin/env python3
"""
Transcribe and Translate Script
This script calls the transcribe and translate API endpoints in sequence:
1. Upload audio file and start transcription
2. Wait for transcription to complete
3. Download the SRT file
4. Upload SRT file and start translation with 3 languages
5. Wait for translation to complete
6. Download the translated SRT files
"""

import requests
import json
import time
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import urllib.request

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

class TranscribeTranslateClient:
    def __init__(self, api_base_url: str, api_key: Optional[str] = None):
        """
        Initialize the client
        
        Args:
            api_base_url: Base URL of the API (e.g., "http://localhost:8000" or "https://your-api-domain.com")
            api_key: Optional API key for authentication
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers['X-API-Key'] = api_key
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.api_base_url}{endpoint}"
        
        # Add headers to kwargs
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers'].update(self.headers)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Status code: {e.response.status_code}")
                print(f"   Response: {e.response.text}")
            raise
    
    def health_check(self) -> bool:
        """Check if the API is accessible by testing a simple endpoint"""
        try:
            # Since there's no health endpoint in the new API spec, we'll test with a simple request
            # that should return an error but confirms the API is reachable
            response = self._make_request('GET', '/api/v1/jobs/invalid-job-id/status')
            return False  # This should fail, but if it doesn't, something is wrong
        except Exception as e:
            # If we get a 404 or similar error, the API is reachable
            if "404" in str(e) or "Not Found" in str(e):
                print(f"✅ API is accessible")
                return True
            else:
                print(f"❌ API health check failed: {e}")
                return False
    
    def start_transcription(self, audio_file_path: str = None, s3_presigned_url: str = None) -> str:
        """
        Start transcription job
        
        Args:
            audio_file_path: Path to the audio file (optional if s3_presigned_url is provided)
            s3_presigned_url: S3 presigned URL for audio file (optional if audio_file_path is provided)
            
        Returns:
            Job ID
            
        Note: Provide either audio_file_path OR s3_presigned_url, not both.
        """
        if not audio_file_path and not s3_presigned_url:
            raise ValueError("Either audio_file_path or s3_presigned_url must be provided")
        
        if audio_file_path and s3_presigned_url:
            raise ValueError("Provide either audio_file_path OR s3_presigned_url, not both")
        
        if s3_presigned_url:
            print(f"🎵 Starting transcription for S3 URL: {s3_presigned_url}")
            data = {'s3_presigned_url': s3_presigned_url}
            response = self._make_request('POST', '/api/v1/transcribe', data=data)
        else:
            print(f"🎵 Starting transcription for: {audio_file_path}")
            
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            with open(audio_file_path, 'rb') as f:
                files = {'file': (os.path.basename(audio_file_path), f, 'audio/mpeg')}
                response = self._make_request('POST', '/api/v1/transcribe', files=files)
        
        job_id = response['job_id']
        print(f"✅ Transcription job started: {job_id}")
        return job_id
    
    def start_translation(self, srt_file_path: str = None, s3_presigned_url: str = None, target_languages: list = None) -> str:
        """
        Start translation job
        
        Args:
            srt_file_path: Path to the SRT file (optional if s3_presigned_url is provided)
            s3_presigned_url: S3 presigned URL for SRT file (optional if srt_file_path is provided)
            target_languages: List of target language codes (default: ["es", "fr", "de"])
            
        Returns:
            Job ID
            
        Note: Provide either srt_file_path OR s3_presigned_url, not both.
        """
        if not srt_file_path and not s3_presigned_url:
            raise ValueError("Either srt_file_path or s3_presigned_url must be provided")
        
        if srt_file_path and s3_presigned_url:
            raise ValueError("Provide either srt_file_path OR s3_presigned_url, not both")
        
        if target_languages is None:
            target_languages = ["es", "fr", "de"]  # Spanish, French, German
        
        print(f"   Target languages: {', '.join(target_languages)}")
        
        if s3_presigned_url:
            print(f"🌐 Starting translation for S3 URL: {s3_presigned_url}")
            data = {
                's3_presigned_url': s3_presigned_url,
                'languages': ','.join(target_languages)
            }
            response = self._make_request('POST', '/api/v1/translate', data=data)
        else:
            print(f"🌐 Starting translation for: {srt_file_path}")
            
            if not os.path.exists(srt_file_path):
                raise FileNotFoundError(f"SRT file not found: {srt_file_path}")
            
            with open(srt_file_path, 'rb') as f:
                files = {'file': (os.path.basename(srt_file_path), f, 'text/plain')}
                # Support both comma-separated string and JSON array as per new API spec
                data = {
                    'languages': ','.join(target_languages)
                }
                response = self._make_request('POST', '/api/v1/translate', files=files, data=data)
        
        job_id = response['job_id']
        print(f"✅ Translation job started: {job_id}")
        return job_id
    
    def wait_for_job_completion(self, job_id: str, job_type: str = "job", timeout_minutes: int = 30) -> bool:
        """
        Wait for job completion
        
        Args:
            job_id: Job ID to monitor
            job_type: Type of job for logging ("transcription" or "translation")
            timeout_minutes: Maximum time to wait in minutes
            
        Returns:
            True if job completed successfully, False if failed or timed out
        """
        print(f"⏳ Waiting for {job_type} completion...")
        
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        
        while True:
            if time.time() - start_time > timeout_seconds:
                print(f"❌ {job_type.capitalize()} job timed out after {timeout_minutes} minutes")
                return False
            
            try:
                status_response = self._make_request('GET', f'/api/v1/jobs/{job_id}/status')
                status = status_response['status']
                progress = status_response.get('progress', 0)
                message = status_response.get('message', '')
                
                print(f"   Status: {status} | {message}")
                
                if status == 'completed':
                    print(f"✅ {job_type.capitalize()} job completed successfully!")
                    return True
                elif status == 'failed':
                    print(f"❌ {job_type.capitalize()} job failed: {message}")
                    return False
                elif status in ['pending', 'processing']:
                    time.sleep(10)  # Wait 10 seconds before checking again
                else:
                    print(f"⚠️  Unknown status: {status}")
                    time.sleep(10)
                    
            except Exception as e:
                print(f"❌ Error checking job status: {e}")
                time.sleep(10)
    
    def get_job_result_urls(self, job_id: str) -> Dict[str, str]:
        """
        Get S3 download URLs for job results without downloading
        
        Args:
            job_id: Job ID
            
        Returns:
            Dictionary mapping file types to S3 URLs
        """
        print(f"🔗 Getting S3 URLs for job: {job_id}")
        
        try:
            result_response = self._make_request('GET', f'/api/v1/jobs/{job_id}/result')
            download_urls = result_response.get('download_urls', {})
            
            print(f"🔍 Available S3 URLs: {list(download_urls.keys())}")
            print()
            
            # Show S3 URLs in logs
            print("🌐 S3 Download URLs:")
            for file_type, url in download_urls.items():
                if url:
                    print(f"   {file_type}: {url}")
            print()
            
            return download_urls
            
        except Exception as e:
            print(f"❌ Error getting result URLs: {e}")
            return {}
    
    def download_job_results(self, job_id: str, output_dir: str = "downloads") -> Dict[str, str]:
        """
        Download job results
        
        Args:
            job_id: Job ID
            output_dir: Directory to save downloaded files
            
        Returns:
            Dictionary mapping file types to local file paths
        """
        print(f"📥 Downloading results for job: {job_id}")
        
        # Create job-specific directory
        job_dir = os.path.join(output_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        print(f"📁 Created job directory: {job_dir}")
        
        try:
            result_response = self._make_request('GET', f'/api/v1/jobs/{job_id}/result')
            download_urls = result_response.get('download_urls', {})
            
            print(f"🔍 Available download URLs: {list(download_urls.keys())}")
            print()
            
            # Show S3 URLs in logs
            print("🌐 S3 Download URLs:")
            for file_type, url in download_urls.items():
                if url:
                    print(f"   {file_type}: {url}")
            print()
            
            downloaded_files = {}
            
            for file_type, url in download_urls.items():
                if url:
                    # Determine file extension based on file type and URL
                    if file_type in ['transcript', 'diarization'] or url.endswith('.srt'):
                        extension = '.srt'
                    elif file_type == 'vtt' or url.endswith('.vtt'):
                        extension = '.vtt'
                    elif file_type == 'json' or url.endswith('.json'):
                        extension = '.json'
                    elif file_type == 'original_audio' or url.endswith(('.mp3', '.wav', '.m4a')):
                        # Extract original file extension from URL
                        if '.mp3' in url:
                            extension = '.mp3'
                        elif '.wav' in url:
                            extension = '.wav'
                        elif '.m4a' in url:
                            extension = '.m4a'
                        else:
                            extension = '.mp3'  # default
                    else:
                        extension = '.txt'
                    
                    # Create filename (without job_id prefix since it's in job directory)
                    filename = f"{file_type}{extension}"
                    file_path = os.path.join(job_dir, filename)
                    
                    print(f"📥 Downloading {file_type}: {filename}")
                    print(f"   From: {url}")
                    
                    # Download file
                    urllib.request.urlretrieve(url, file_path)
                    downloaded_files[file_type] = file_path
                    print(f"   ✅ Downloaded: {file_path}")
                    print()
            
            return downloaded_files
            
        except Exception as e:
            print(f"❌ Error downloading results: {e}")
            return {}

def main():
    """Main function"""
    # Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://34.212.19.243:8000')
    API_KEY = os.getenv('API_KEY', None)
    AUDIO_FILE = os.getenv('AUDIO_FILE', 'loop.mp3')
    AUDIO_S3_URL = os.getenv('AUDIO_S3_URL', None)
    SRT_S3_URL = os.getenv('SRT_S3_URL', None)  # For direct SRT translation
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'downloads')
    TRANSLATION_LANGUAGES = os.getenv('TRANSLATION_LANGUAGES', 'es,fr,de').split(',')
    JOB_TIMEOUT = int(os.getenv('JOB_TIMEOUT', '30'))
    
    print("🎵 Transcribe and Translate Script")
    print("=" * 50)
    print(f"API Base URL: {API_BASE_URL}")
    if AUDIO_S3_URL:
        print(f"Audio S3 URL: {AUDIO_S3_URL}")
    else:
        print(f"Audio File: {AUDIO_FILE}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Translation Languages: {', '.join(TRANSLATION_LANGUAGES)}")
    print()
    
    # Initialize client
    client = TranscribeTranslateClient(API_BASE_URL, API_KEY)
    
    # Check API health
    if not client.health_check():
        print("❌ API is not healthy. Exiting.")
        sys.exit(1)
    
    print()
    
    try:
        # Step 1: Start transcription
        if AUDIO_S3_URL:
            transcription_job_id = client.start_transcription(s3_presigned_url=AUDIO_S3_URL)
        else:
            transcription_job_id = client.start_transcription(audio_file_path=AUDIO_FILE)
        print()
        
        # Step 2: Wait for transcription to complete
        if not client.wait_for_job_completion(transcription_job_id, "transcription", JOB_TIMEOUT):
            print("❌ Transcription failed. Exiting.")
            sys.exit(1)
        print()
        
        # Step 3: Download transcription results
        transcription_files = client.download_job_results(transcription_job_id, OUTPUT_DIR)
        print()
        
        if not transcription_files:
            print("❌ No transcription files downloaded. Exiting.")
            sys.exit(1)
        
        # Find the SRT file for translation (prefer transcript, then diarization)
        srt_file = None
        preferred_types = ['transcript', 'diarization']
        
        # First try to find transcript or diarization files
        for preferred_type in preferred_types:
            if preferred_type in transcription_files:
                srt_file = transcription_files[preferred_type]
                print(f"📄 Using {preferred_type} file for translation: {srt_file}")
                break
        
        # If not found, look for any .srt file
        if not srt_file:
            for file_type, file_path in transcription_files.items():
                if file_path.endswith('.srt'):
                    srt_file = file_path
                    print(f"📄 Using {file_type} file for translation: {srt_file}")
                    break
        
        if not srt_file:
            print("❌ No SRT file found in transcription results. Available files:")
            for file_type, file_path in transcription_files.items():
                print(f"   - {file_type}: {file_path}")
            sys.exit(1)
        
        # This line is now handled in the logic above
        print()
        # Step 4: Start translation
        if SRT_S3_URL:
            # Use S3 URL for translation instead of downloaded file
            print(f"🌐 Using S3 URL for translation: {SRT_S3_URL}")
            translation_job_id = client.start_translation(s3_presigned_url=SRT_S3_URL, target_languages=TRANSLATION_LANGUAGES)
        else:
            # Use downloaded SRT file for translation
            translation_job_id = client.start_translation(srt_file_path=srt_file, target_languages=TRANSLATION_LANGUAGES)
        print()
        
        # Step 5: Wait for translation to complete
        if not client.wait_for_job_completion(translation_job_id, "translation", JOB_TIMEOUT):
            print("❌ Translation failed. Exiting.")
            sys.exit(1)
        print()
        
        # Step 6: Download translation results
        translation_files = client.download_job_results(translation_job_id, OUTPUT_DIR)
        print()
        
        # Summary
        print("📋 Summary:")
        print(f"   Transcription Job ID: {transcription_job_id}")
        print(f"   Translation Job ID: {translation_job_id}")
        print(f"   Transcription Files: {len(transcription_files)}")
        print(f"   Translation Files: {len(translation_files)}")
        print(f"   Output Directory: {os.path.abspath(OUTPUT_DIR)}")
        print()
        print("📁 Files organized in job directories:")
        print(f"   Transcription: {os.path.abspath(OUTPUT_DIR)}/{transcription_job_id}/")
        print(f"   Translation: {os.path.abspath(OUTPUT_DIR)}/{translation_job_id}/")
        print()
        print("🎉 All jobs completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
