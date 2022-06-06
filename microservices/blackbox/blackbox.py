from pathlib import Path
import os
import socket
import requests
from aiohttp import web

LOCAL_IP = socket.gethostbyname(socket.gethostname())
HOST= os.getenv("BLACKBOX_HOST", "0.0.0.0")
PORT = os.getenv("BLACKBOX_PORT", 2230)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
REG_PORT = os.getenv("SR_PORT", 55555)
SERVICE = os.path.basename(__file__).rstrip(".py")


def routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/", info),
            web.get("/info", info)
        ]
    )


async def info(request) -> web.json_response:
    """
    This will return the blackbox's info
    """
    response_data = {"local_ip": LOCAL_IP, "port": PORT, "version": "v2", "service_registry_address": REG_ADDR, "service_registry_port": REG_PORT}
    response = web.json_response(response_data)
    return response


def register(service):
    print(f"Getting: http://{REG_ADDR}:{REG_PORT}/add/{service}/{LOCAL_IP}/{PORT}")
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/add/{service}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


def unregister(service):
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/remove/{service}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


def main():
    print("The menu microservice web server is starting up!")
    app = web.Application()
    routes(app)
    try:
        register(SERVICE)
    except requests.exceptions.ConnectionError as err:
        print(err)
    try:
        web.run_app(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        unregister(SERVICE)


if __name__ == "__main__":
    main()
