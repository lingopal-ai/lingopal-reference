# 🚀 Lingopal WebSocket Client

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

### 3. 📥 Install the WebSocket Client

Install the package in editable/development mode:

```bash
pip install -e .
```

---

## 🧪 Usage

Run the example WebSocket client script:

```bash
python examples/run_client.py <stream_id> <api_key> [env]
python examples/run_client.py 06841c36-4c8c-719e-8000-0caa443828fc e2f27925d60b4c1fa954c17a2e1bc8f5
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

## 🛠 Notes

- The client uses the `websockets` library.
- If connection fails due to a missing header argument, make sure you're using `websockets>=11.0`.
- Example script is located at `examples/run_client.py`.


# ▶️ Start a Stream via API (Optional)

You can use `examples/start_stream.py` to initiate a stream via the Lingopal API.

### Required Environment Variables:

- `LINGOPAL_API_KEY`: Your API key for authentication
- `LINGOPAL_INGEST_URL`: The SRT ingest URL (e.g., `srt://your.server:7070`)

### Example:

```bash
export LINGOPAL_API_KEY="your-api-key"
export LINGOPAL_INGEST_URL="srt://your.srt.server:7070"

python examples/start_stream.py
