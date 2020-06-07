import asyncio
import json
import logging
import socket
import sys

import requests
import websockets

SLEEP_TIMEOUT = 5
SLEEP_STEP = 0.1
LOCAL_PORT = 20080
API_PROTO = "http://"
API_SERVER = ""
API_PATH = "/go-CP"
TEMPERATURE_ENDPOINTS = {
    "temp_cauldron": "/updateTemp-28-021600873fff",
    "temp_heater": "/updateTemp-28-021600a351ff"
}
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def frange(start, stop, step=1.0):
    while start < stop:
        yield start
        start += step


async def producer():
    url = API_PROTO + API_SERVER + API_PATH
    data = {k: requests.get(f'{url}{v}').content.decode().strip() for k, v in TEMPERATURE_ENDPOINTS.items()}
    return json.dumps(data)


async def hello(websocket, path):
    client = ":".join(str(i) for i in websocket.remote_address)
    try:
        LOGGER.info(f"Client came: {client}")
        while True:
            message = await producer()
            LOGGER.info(f"Sending {message} to {client}")
            await websocket.send(message)
            for i in frange(0, SLEEP_TIMEOUT, SLEEP_STEP):
                if websocket.closed:
                    raise websockets.exceptions.ConnectionClosedError(websocket.close_code, websocket.close_reason)
                await asyncio.sleep(SLEEP_STEP)
    except websockets.exceptions.ConnectionClosedError:
        LOGGER.info(f"Client gone: {client}")


if __name__ == "__main__":
    API_SERVER = sys.argv[1]
    try:
        LOCAL_PORT = sys.argv[2]
    except IndexError:
        pass
    finally:
        LOGGER.info(f"Using port {LOCAL_PORT}")

    start_server = websockets.serve(hello, socket.gethostname(), LOCAL_PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
