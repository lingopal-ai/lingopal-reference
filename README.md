# 🚀 Lingopal WebSocket Client

A simple Python client that connects to the **Lingopal transcription WebSocket service** using your stream ID and API key.

---

## 📦 Installation

### 1. ✅ Make sure Python 3.8+ is installed

Check your Python version:
```bash
python3 --version
```

If you don’t have Python, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

---

### 2. 🔧 Clone or Download the Project

If you downloaded this as a ZIP:
```bash
unzip lingopal_ws_client_package.zip
cd lingopal_ws_client_package
```

Or clone it via Git (optional):
```bash
git clone https://github.com/your-org/lingopal-ws-client.git
cd lingopal-ws-client
```

---

### 3. 📁 Set Up and Activate a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

---

### 4. 📥 Install the WebSocket Client

```bash
pip install -e .
```

---

## 🧪 Usage

Run the example client:

```bash
python examples/run_client.py <stream_id> <api_key>
```

**Arguments:**
- `<stream_id>`: The stream UUID you get from Lingopal
- `<api_key>`: Your personal Lingopal API key
- `[env]` *(optional)*:
  - Use `prod` for production (default)
  - Use `dev` for localhost testing

---

### 🧷 Example

```bash
python examples/run_client.py 0684xxxx-xxxx-xxxx-xxxx a9e12xxxxxxx
```

This will:
- Connect to the transcription WebSocket server
- Send a test message
- Print any transcription messages received

---

## 🌐 Environments

| Env   | URL Base                                               |
|--------|--------------------------------------------------------|
| `prod` | `wss://streaming.lingopal.ai/v1/live/transcription`   |

