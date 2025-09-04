# 🚀 Lingopal Cookbook

This repository contains a simple Python client that connects to the **Lingopal transcription WebSocket service** using your stream ID and API key.

📍 GitHub Repo: [https://github.com/lingopal-ai/lingopal-reference](https://github.com/lingopal-ai/lingopal-reference)

---

## 📦 Installation

### 1. ✅ Make sure Python 3.8+ is installed

Check your Python version:
```bash
python3 --version
```

If you don’t have Python, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

---

### 2. 📁 Set Up and Activate a Virtual Environment

In the root of this repo:

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

---

### 3. 📥 Install the dependencies

Install the package in editable/development mode:

```bash
pip install -e .
```

---


# ▶️ Start a Stream via API

You can use `examples/start_stream.py` to initiate a stream via the Lingopal API.

### Required Environment Variables:

- `LINGOPAL_API_KEY`: Your API key for authentication
- `LINGOPAL_INGEST_URL`: The SRT ingest URL (e.g., `srt://your.server:7070`)

### Example:

```bash
export LINGOPAL_API_KEY="your-api-key"
export LINGOPAL_INGEST_URL="srt://your.srt.server:7070"

python examples/start_stream.py
```

---

# 📅 Schedule a Stream via API

You can use `examples/schedule_stream.py` to schedule a stream for later execution via the Lingopal API.

### Required Environment Variables:

- `LINGOPAL_API_KEY`: Your API key for authentication

### Command Line Arguments:

- `ingest_url`: The SRT ingest URL (e.g., `srt://your.server:7070`)
- `scheduled_time`: The scheduled start time in ISO 8601 format (e.g., `2024-01-15T10:00:00`)
- `timezone`: Regional timezone for the scheduled time (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`)

### Example:

```bash
export LINGOPAL_API_KEY="your-api-key"

python examples/schedule_stream.py --ingest_url "srt://your.srt.server:7070" --scheduled_time "2024-01-15 10:00:00" --timezone "America/New_York"
```

### Usage Examples:

```bash
# Schedule a stream for New York timezone
python examples/schedule_stream.py --ingest_url "srt://stream.example.com:8080" --scheduled_time "2024-01-20 14:30:00" --timezone "America/New_York"

# Schedule a stream for London timezone
python examples/schedule_stream.py --ingest_url "srt://live.server:9090" --scheduled_time "2024-02-01 09:00:00" --timezone "Europe/London"

# Schedule a stream for Tokyo timezone
python examples/schedule_stream.py --ingest_url "srt://asia.stream:7070" --scheduled_time "2024-01-25 18:00:00" --timezone "Asia/Tokyo"
```

### ⏰ Timezone Guidelines:

**Use regional timezones instead of UTC offsets:**
- ✅ **Good**: `America/New_York`, `Europe/London`, `Asia/Tokyo`, `Australia/Sydney`
- ❌ **Avoid**: `UTC`, `UTC+5`, `EST`, `PST`

**Common Regional Timezones:**
- **North America**: `America/New_York`, `America/Chicago`, `America/Denver`, `America/Los_Angeles`
- **Europe**: `Europe/London`, `Europe/Paris`, `Europe/Berlin`, `Europe/Moscow`
- **Asia**: `Asia/Tokyo`, `Asia/Shanghai`, `Asia/Singapore`, `Asia/Dubai`
- **Australia**: `Australia/Sydney`, `Australia/Melbourne`, `Australia/Perth`

### Key Features:

- **Scheduled Execution**: Set a specific time for stream start using `scheduled_time` (ISO 8601 format)
- **Voice Cloning**: Enable AI voice cloning with `voice_cloning: true`
- **Lipsync**: Enable lip synchronization with `lipsync: true`
- **Customizable Audio**: Configure vocals track, background track, and mix levels
- **Caption Support**: Optional 708/608 caption generation
- **Multi-language**: Support for source and destination language configuration
- **Stream-livee**: In order to have a live stream at your time, Please schedule stream 10 minutes before. So that it can be live at that moment

# 🚀 Lingopal WebSocket Client

Run the example WebSocket client script:

```bash
python examples/run_client.py <stream_id> <api_key>
```

**Arguments:**
- `<stream_id>`: The stream UUID you get from Lingopal
- `<api_key>`: Your Lingopal API key
- `[env]` *(optional)*:
  - `prod` (default): connect to production

---

### 🧷 Example

```bash
python examples/run_client.py 0684xxxx-xxxx-xxxx-xxxx a9e12xxxxxxx
```

This will:
- Connect to the transcription WebSocket server
- Print any messages received from the server

---

## 🌐 Environments

| Env   | URL Base                                               |
|--------|--------------------------------------------------------|
| `prod` | `wss://streaming.lingopal.ai/v1/live/transcription`   |

---

# 🎯 Translation & Transcription Examples

The `examples/translation_transcription_examples/` folder contains comprehensive examples for using the Audio Transcription & Translation API.

## Quick Start

1. **Navigate to the examples folder:**
```bash
cd examples/translation_transcription_examples
```

2. **Set up your environment:**
```bash
python setup.py
```

3. **Edit the `.env` file with your configuration:**
```bash
# API Configuration
API_BASE_URL=http://34.212.19.243:8000
API_KEY=your-api-key-here

# File Configuration
AUDIO_FILE=path/to/your/audio.mp3
OUTPUT_DIR=downloads

# Translation Configuration
TRANSLATION_LANGUAGES=es,fr,de
```

4. **Run the full transcription and translation pipeline:**
```bash
python transcribe_and_translate.py
```

## What's Included

- **`transcribe_and_translate.py`**: Complete pipeline script for audio transcription and translation
- **`setup.py`**: Automated environment setup and dependency installation
- **`README_client.md`**: Detailed documentation for the client scripts
- **Sample audio files**: Test audio files for trying out the API
- **Environment templates**: Easy configuration setup

## Features

- **Audio Transcription**: Upload audio files and get SRT transcripts with speaker diarization
- **Multi-language Translation**: Translate SRT files to multiple target languages
- **Environment Configuration**: Easy setup using .env files


For detailed usage instructions, see [`examples/translation_transcription_examples/README_client.md`](examples/translation_transcription_examples/README_client.md).

---

## 🛠 Notes

- The client uses the `websockets` library.
- If connection fails due to a missing header argument, make sure you're using `websockets>=11.0`.
- Example script is located at `examples/run_client.py`.

