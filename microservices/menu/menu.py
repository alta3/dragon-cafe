from pathlib import Path
import os
import jinja2
import socket
import requests
from aiohttp import web

HOST = os.getenv("MENU_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("MENU_PORT", 2227)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
#REG_ADDR = "10.17.133.17"
REG_PORT = os.getenv("SR_PORT", 55555)
SERVICE = os.path.basename(__file__).rstrip(".py")

class Page:
    def __init__(self, filename, templates_dir=Path("templates"), args={}, cookies={}):
        """
        Create a new instance of an html page to be returned
        :param fillename: name of file found in the templates_dir
        """
        self.path = templates_dir
        self.file = templates_dir / filename
        self.args = args
        self.cookies = cookies

    def render(self):
        with open(self.file) as f:
            txt = f.read()
            print(f"Templating in {self.args}")
            j2 = jinja2.Template(txt).render(self.args)
            resp = web.Response(text=j2, content_type='text/html')
            for c, j in self.cookies:
                resp.set_cookie(c, j)
            return resp

def routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/", menu),
            web.get("/menu", menu)
        ]
    )


async def menu(request) -> web.Response:
    """
    This will return the menu
    """
    food_items = [
        {"item": "General Tzo's Chicken", "description": "Yummy chicken on rice", "price": 12.99},
        {"item": "Kung Pao Beef", "description": "Spicy Beef on rice", "price": 13.99}
    ]  # TODO - Update to a sqlite3 database call
    args = {"foods": food_items}
    page = Page(filename="menu.html", args=args)
    return page.render()


def register(service):
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
