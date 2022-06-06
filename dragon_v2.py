#!/usr/bin/env python3

"""
Dragon Cafe Microservice Application | Author: Sam Griffith | Org: Alta3 Research Inc.

This application is an example Chinese Restaurant website.

It consists of three distinct microservices:

    - a login form
    - a menu
    - a fortune cookie emulator
"""

from aiohttp import web
import jinja2
from pathlib import Path
import os
import requests
import socket

HOST = os.getenv("DRAGON_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("DRAGON_PORT", 2225)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")                                   
REG_PORT = os.getenv("SR_PORT", 55555)
SERVICE = __file__.rstrip(".py")


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
            web.get("/", home),
            web.get("/login", login_v2),
            web.get("/login/{ex_path}", login_v2),
            web.post("/login/{ex_path}", login_v2),
            web.get("/fortune_cookie", fortune_cookie_v2),
            web.get("/fortune_cookie/{ex_path}", fortune_cookie_v2),
            web.get("/menu", menu_v2),
        ]
    )


async def login_v2(request) -> web.Response:
    print(request)
    ex_path = request.match_info.get('ex_path', '')
    if request.method == "GET":
        if ex_path:
            r = requests.get(f"http://v2.dragon-cafe.com/login/{ex_path}")
        else:
            r = requests.get(f"http://v2.dragon-cafe.com/login")
    if request.method == "POST":
        print("Attempting to POST!")
        payload = await request.post()
        r = requests.post(f"http://v2.dragon-cafe.com/login/{ex_path}", data=payload)
    return web.Response(text=r.text, content_type='text/html')


async def fortune_cookie_v2(request) -> web.Response:
    print(request)
    ex_path = request.match_info.get('ex_path', '')
    if ex_path == '':
        print("This one")
        r = requests.get("http://v2.dragon-cafe.com/fortune_cookie")
    else:
        print("That one")
        r = requests.get(f"http://v2.dragon-cafe.com/fortune_cookie/{ex_path}")
    return web.Response(text=r.text, content_type='text/html')


async def menu_v2(request) -> web.Response:
    print(request)
    r = requests.get("http://v2.dragon-cafe.com/menu")
    return web.Response(text=r.text, content_type='text/html')


async def home(request) -> web.Response:
    """
    This is the home page for the website
    """
    print(request)
    page = Page(filename="index.html")
    return page.render()


async def register(handled: str = '') -> None:
    print(f"This has been handled: {handled}")
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/add/{SERVICE}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


async def unregister(handled: str = '') -> None:
    print(f"This has been handled: {handled}")
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/remove/{SERVICE}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


def main():
    """
    This is the main process for the aiohttp server.

    This works by instantiating the app as a web.Application(),
    then applying the setup function we built in our routes
    function to add routes to our app, then by starting the async
    event loop with web.run_app().
    """

    print("This aiohttp web server is starting up!")
    app = web.Application()
    routes(app)
    app.on_startup.append(register)
    app.on_shutdown.append(unregister)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
