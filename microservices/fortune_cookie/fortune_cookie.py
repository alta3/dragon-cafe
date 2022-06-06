from pathlib import Path
import os
import jinja2
import socket
import random
import requests
from aiohttp import web

HOST = os.getenv("FORTUNE_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("FORTUNE_PORT", 2229)
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
            web.get("/", closed_cookie),
            web.get("/fortune_cookie", closed_cookie),
            web.get("/fortune", fortune),
            web.get("/fortune_cookie/fortune", fortune),

        ]
    )


async def closed_cookie(request) -> web.Response:
    """
    This is the primary landing page for the fortune service.
    """
    print(request)
    page = Page(filename="cookie.html")
    return page.render()


async def fortune(request) -> web.Response:
    """
    This is the primary landing page for the fortune service.
    """

    possible = [
        "People are naturally attracted to you.",
        "You learn from your mistakes... You will learn a lot today.",
        "If you have something good in your life, don't let it go!",
        "What ever you're goal is in life, embrace it visualize it, and for it will be yours.",
        "Your shoes will make you happy today.",
        "You cannot love life until you live the life you love.",
        "Be on the lookout for coming events; They cast their shadows beforehand.",
        "Land is always on the mind of a flying bird.",
        "The man or woman you desire feels the same about you.",
        "Meeting adversity well is the source of your strength.",
        "A dream you have will come true.",
        "Our deeds determine us, as much as we determine our deeds.",
        "Never give up. You're not a failure if you don't give up.",
        "You will become great if you believe in yourself.",
        "There is no greater pleasure than seeing your loved ones prosper.",
        "You will marry your lover.",
        "A very attractive person has a message for you.",
        "You already know the answer to the questions lingering inside your head.",
        "It is now, and in this world, that we must live.",
        "You must try, or hate yourself for not trying.",
        "You can make your own happiness.",
        "The greatest risk is not taking one.",
        "The love of your life is stepping into your planet this summer.",
        "Love can last a lifetime, if you want it to.",
        "Adversity is the parent of virtue.",
        "Serious trouble will bypass you.",
        "A short stranger will soon enter your life with blessings to share.",
        "Now is the time to try something new.",
        "Wealth awaits you very soon.",
        "If you feel you are right, stand firmly by your convictions.",
        "If winter comes, can spring be far behind?",
        "Keep your eye out for someone special.",
        "You are very talented in many ways.",
        "A stranger, is a friend you have not spoken to yet.",
        "A new voyage will fill your life with untold memories.",
        "You will travel to many exotic places in your lifetime.",
        "Your ability for accomplishment will follow with success.",
        "Nothing astonishes men so much as common sense and plain dealing.",
        "Its amazing how much good you can do if you dont care who gets the credit.",
        "Everyone agrees. You are the best.",
        "Life consist not in holding good cards, but in playing those you hold well.",
        "Jealousy doesn't open doors, it closes them!",
        "It's better to be alone sometimes.",
        "When fear hurts you, conquer it and defeat it!",
        "Let the deeds speak.",
        "You will be called in to fulfill a position of high honor and responsibility.",
        "The man on the top of the mountain did not fall there.",
        "You will conquer obstacles to achieve success.",
        "Joys are often the shadows, cast by sorrows.",
        "Fortune favors the brave.",
    ]
    fortune = random.choice(possible)
    args = {"fortune": fortune}
    page = Page(filename="seer.html", args=args)
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
