#!/usr/bin/env python3

"""
An example monolith to practice verifying
the code is able to receive a request on
the /v2/menu path and route it to the menu
microservice.
"""

# Best practice advises us to import Standard Library packages first
import json

# Best practice advises us to put a blank line between Standard Library and 3rd Party Packages
from aiohttp import web
import requests


def routes(app):
    """ Add in a route """
    app.add_routes(
            [
                web.get("/v2/menu", menu_v2)
            ]
        )


async def menu_v2(request) -> web.Response:
    """
    A new version of the menu function which will first ask our Service Registry
    for an instance of the menu, and then perform a request to that instance
    """
    print(request)
    # Ask the Service Registry for an instance of the menu service
    menu_svc = requests.get("http://127.0.0.1:55555/get_one/menu").text
    print(menu_svc)
    menu_host = json.loads(menu_svc)
    # assign vars for the ip and port
    menu_ip = menu_host['endpoints'][0]
    menu_port = menu_host['endpoints'][1]
    # Send a request to the menu service instance
    r = requests.get(f"http://{menu_ip}:{menu_port}/menu")
    # return the response that was just received
    return web.Response(text=r.text, content_type='text/html')


def main():
    app = web.Application()
    routes(app)
    web.run_app(app, host="0.0.0.0", port=3030)


if __name__ == "__main__":
    main()
