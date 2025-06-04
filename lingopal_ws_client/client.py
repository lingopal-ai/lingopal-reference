import asyncio
import websockets

ENV_URLS = {
    "prod": "wss://streaming.lingopal.ai/v1/live/transcription",
}

async def connect_to_server(stream_id: str, api_key: str, env: str = "prod"):
    base_url = ENV_URLS.get(env, ENV_URLS["prod"])
    url = f"{base_url}/{stream_id}"

    headers = {"X-API-Key": api_key}

    try:
       async with websockets.connect(url, additional_headers=headers) as websocket:
            print(f"Connected to {url}")
            # Loop to receive messages
            while True:
                try:
                    message = await websocket.recv()
                    print(f"Received from server: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed by server.")
                    break

    except Exception as e:
        print(f"Connection failed: {e}")
