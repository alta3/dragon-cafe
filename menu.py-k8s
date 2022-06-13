#!/usr/bin/env python3

"""
Dragon Cafe Menu Microservice | Author: Sam Griffith | Org: Alta3 Research Inc.

This Menu Microservice is the first part of the monolithic application of a Chinese Restaurant website that has been broken out into it's own service.
"""

from aiohttp import web
import jinja2
from pathlib import Path
import os

# Environmental Variables    
HOST = os.getenv("MENU_HOST", "0.0.0.0")
PORT = os.getenv("PORT_DE_MENU", 2227)

# Establish a new object type, called a Page
class Page:
    def __init__(self, filename, templates_dir=Path("templates"), args={}, cookies={}):
        """
        Create a new instance of an html page to be returned
        :param filename: name of file found in the templates_dir
        """
        self.path = templates_dir
        self.file = templates_dir / filename
        self.args = args
        self.cookies = cookies

    def render(self):
        """
        Open a Jinja2 formatted template file, and return
        the filled in file as a web.Response object
        :return: web.Response
        """
        with open(self.file) as f:
            txt = f.read()
            print(f"Templating in {self.args}")
            # Fill in the template file with any args provided
            j2 = jinja2.Template(txt).render(self.args)
            # Create a response object
            resp = web.Response(text=j2, content_type='text/html')
            # Add any cookies passed to this page as cookies in the response
            for c, j in self.cookies:
                resp.set_cookie(c, j)
            # feed back the web.Response object with the filled out page
            return resp


def routes(app: web.Application) -> None:
    app.add_routes(
        [
            # web.get == HTTP GET
            web.get("/", menu),
            web.get("/menu", menu)
        ]
    )


async def menu(request) -> web.Response:
    """
    This will return the jinja2 templated menu.html file.
    """
    print(request)
    # Basic food items in a list
    food_items = [
        {"item": "General Tzo's Chicken", "description": "Yummy chicken on rice", "price": 12.99},
        {"item": "Kung Pao Beef", "description": "Spicy Beef on rice", "price": 13.99}
    ]  # TODO - Update to a sqlite3 database call
    args = {"foods": food_items}
    # Create a page from the menu.html template
    page = Page(filename="menu.html", args=args)
    # Render and return the page
    return page.render()


def main():
    """
    This is the main process for the aiohttp server.

    This works by instantiating the app as a web.Application(),
    then applying the setup function we built in our routes
    function to add routes to our app, then by starting the async
    event loop with web.run_app().
    """

    print("This aiohttp web server is starting up!")
    # Create a web.Application object
    app = web.Application()
    # Add the available routes to our web application
    routes(app)
    # Start the webserver
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()

