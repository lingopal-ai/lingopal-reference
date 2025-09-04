# Transcribe and Translate Client Script

This Python script provides a client for the Audio Transcription & Translation API. It allows you to:

1. Upload an audio file and start transcription
2. Wait for transcription to complete
3. Download the SRT subtitle file
4. Upload the SRT file and start translation with multiple languages
5. Wait for translation to complete
6. Download the translated SRT files

## Features

- **Sequential Processing**: Automatically handles the full pipeline from audio to translated subtitles
- **Progress Monitoring**: Real-time status updates with progress percentages
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Configurable**: Support for environment variables and .env file configuration
- **Multiple Languages**: Translate to multiple target languages in a single job
- **File Management**: Automatic download and organization of result files
- **Dotenv Support**: Easy configuration using .env files

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_client.txt
```

2. Set up your configuration (see Configuration section below)

3. Make sure you have access to the deployed API (update the API base URL in your configuration)

## Usage


```bash
python transcribe_and_translate.py
```

This will use default settings:
- API Base URL: `http://34.212.19.243:8000`
- Audio File: `loop.mp3`
- Output Directory: `downloads`
- Translation Languages: Spanish, French, German

### Using Environment Variables

Set environment variables for customization:

```bash
export API_BASE_URL="http://34.212.19.243:8000"
export API_KEY="your-api-key"
export AUDIO_FILE="path/to/your/audio.mp3"
export OUTPUT_DIR="my_downloads"
export TRANSLATION_LANGUAGES="es,fr,de,it,pt"

python transcribe_and_translate.py
```

### Using S3 Presigned URLs

You can also use S3 presigned URLs instead of local files:

```bash
export API_BASE_URL="http://34.212.19.243:8000"
export API_KEY="your-api-key"
export AUDIO_S3_URL="https://your-bucket.s3.amazonaws.com/path/to/audio.mp3?presigned-params"
export OUTPUT_DIR="my_downloads"
export TRANSLATION_LANGUAGES="es,fr,de,it,pt"

python transcribe_and_translate.py
```

### Using S3 for Translation Only

You can also use an S3 presigned URL for the SRT file to skip transcription and go directly to translation:

```bash
export API_BASE_URL="http://34.212.19.243:8000"
export API_KEY="your-api-key"
export SRT_S3_URL="https://your-bucket.s3.amazonaws.com/path/to/subtitles.srt?presigned-params"
export OUTPUT_DIR="my_downloads"
export TRANSLATION_LANGUAGES="es,fr,de,it,pt"

python transcribe_and_translate.py
```

### Getting S3 URLs Only

You can also get just the S3 URLs without downloading the files:

```bash
# Get S3 URLs for a specific job
python get_s3_urls.py <job_id>

# Or set JOB_ID environment variable
export JOB_ID="your-job-id"
python get_s3_urls.py
```

### Programmatic Usage

```python
from transcribe_and_translate import TranscribeTranslateClient

# Initialize client
client = TranscribeTranslateClient(
    api_base_url="http://34.212.19.243:8000",
    api_key="your-api-key"
)

# Start transcription (using local file)
transcription_job = client.start_transcription(audio_file_path="audio.mp3")

# Or start transcription (using S3 URL)
# transcription_job = client.start_transcription(s3_presigned_url="https://your-bucket.s3.amazonaws.com/audio.mp3?presigned-params")

# Wait for completion
if client.wait_for_job_completion(transcription_job, "transcription"):
    # Get S3 URLs without downloading
    s3_urls = client.get_job_result_urls(transcription_job)
    
    # Or download results to local files
    files = client.download_job_results(transcription_job, "downloads")
    
    # Find SRT file for translation
    srt_file = files.get('transcript') or files.get('diarization')
    if srt_file:
        # Start translation (using local file)
        translation_job = client.start_translation(srt_file_path=srt_file, target_languages=["es", "fr", "de"])
        
        # Or start translation (using S3 URL)
        # translation_job = client.start_translation(s3_presigned_url="https://your-bucket.s3.amazonaws.com/subtitles.srt?presigned-params", target_languages=["es", "fr", "de"])
        
        # Wait for translation
        if client.wait_for_job_completion(translation_job, "translation"):
            # Download translation results
            translation_files = client.download_job_results(translation_job, "downloads")
            print("Pipeline completed!")
```

## Configuration

### Using .env File (Recommended)

1. Copy the example environment file:
```bash
cp env_example.txt .env
```

2. Edit the `.env` file with your settings:
```bash
# API Configuration
API_BASE_URL=http://34.212.19.243:8000
API_KEY=your-api-key-here

# File Configuration
AUDIO_FILE=path/to/your/audio.mp3
OUTPUT_DIR=downloads

# Translation Configuration
TRANSLATION_LANGUAGES=es,fr,de

# Optional: Job timeout (in minutes)
JOB_TIMEOUT=30
```

3. The script will automatically load these variables when you run it.

### Using Environment Variables

Set environment variables for customization:

```bash
export API_BASE_URL="http://34.212.19.243:8000"
export API_KEY="your-api-key"
export AUDIO_FILE="path/to/your/audio.mp3"
export OUTPUT_DIR="my_downloads"
export TRANSLATION_LANGUAGES="es,fr,de,it,pt"

python transcribe_and_translate.py
```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `http://34.212.19.243:8000` | Base URL of the API |
| `API_KEY` | `None` | API key for authentication (if required) |
| `AUDIO_FILE` | `loop.mp3` | Path to the audio file to transcribe |
| `AUDIO_S3_URL` | `None` | S3 presigned URL for audio file (alternative to AUDIO_FILE) |
| `SRT_S3_URL` | `None` | S3 presigned URL for SRT file translation (skips transcription) |
| `OUTPUT_DIR` | `downloads` | Directory to save downloaded files |
| `TRANSLATION_LANGUAGES` | `es,fr,de` | Comma-separated list of target language codes |
| `JOB_TIMEOUT` | `30` | Maximum time to wait for job completion (minutes) |


The script creates the following directory structure:

```
downloads/
├── {transcription_job_id}/                  # Transcription job folder
│   ├── transcript.srt                       # Original transcription
│   ├── diarization.srt                      # Speaker diarization
│   ├── original_audio.mp3                   # Original audio file
│   └── vtt.vtt                             # VTT format (if available)
└── {translation_job_id}/                    # Translation job folder
    ├── es.srt                               # Spanish translation
    ├── fr.srt                               # French translation
    ├── de.srt                               # German translation
    └── original.srt                         # Original SRT file used for translation
```
