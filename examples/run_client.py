import asyncio
import sys
from lingopal_ws_client.client import connect_to_server

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_client.py <stream_id> <api_key> [env]")
        sys.exit(1)

    stream_id = sys.argv[1]
    api_key = sys.argv[2]
    env = sys.argv[3] if len(sys.argv) > 3 else "prod"

    asyncio.run(connect_to_server(stream_id, api_key, env))
