from pathlib import Path
import os
import jinja2
import requests
from aiohttp import web

HOST = os.getenv("LOGIN_HOST", "0.0.0.0")
PORT = os.getenv("LOGIN_PORT", 2227)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
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
            web.get("/", login),
            web.get("/login", login),
            web.post("/logging_in", logging_in),
            web.post("/login/logging_in", logging_in)
        ]
    )


async def logging_in(request):
    print(f"logging_in: {request}")
    if request.method == 'POST':
        data = await request.post()
        name = data['name']
        print("POSTED")
        print(name)
        # TODO - Add authentication logic
        poodle = await login(request, name=name)
        return poodle


async def login(request, name=None):
    """
    This is the login page for the website
    """
    print(f"login: {request}")
    # if request.query.get('name') is not None:
    if name is not None:
        print("We got something here!")
        # TODO - Add authentication logic
        resp = web.Response(text=name)
        page = Page(filename="hello.html", args={"name": name})
        print("Cookies Set?")
        return page.render()
    else:
        print("No name has been sent yet!")
        args = {"name": name}
        page = Page(filename="login.html", args=args)
        return page.render()


def main():
    print("The menu microservice web server is starting up!")
    app = web.Application()
    routes(app)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
