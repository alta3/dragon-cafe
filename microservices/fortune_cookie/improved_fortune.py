#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
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
            web.static("/fortune_cookie/fortune_cookie_images/", "images"),
        ]
    )



async def closed_cookie(request) -> web.Response:
    """
    This is the primary landing page for the fortune service.
    """
    print(request)
    page = Page(filename="cookie.html")
    return page.render()

def fortune_builder(txt):
    words = txt.split()
    lines = []
    line_length = 0
    line = ""
    line_limit = 28
    for word in words:
        word_length = len(word)
        if (line_length + word_length + 1) < line_limit:
            line_length += word_length + 1
            line += f"{word} "
        else:
            lines.append(line)
            line_length = 0
            line_limit -= 7
            line = f"{word} "
    if line not in lines:
        lines.append(line)
    lines = [line.strip() for line in lines]
    return lines


def amorphism(lines, size):
    cookie_pic_int = random.randint(1, 99999)
    fnt = ImageFont.truetype('arial.ttf', 70)
    img2 = Image.new('RGBA', size, color="WHITE")
    d = ImageDraw.Draw(img2)
    across = 450
    down = 315
    for line in lines:
        d.text((across, down), line, font=fnt, fill=(0, 0, 0))
        across += 100
        down += 75
    img2 = img2.rotate(350)

    # Turning White cells transparent
    data2 = img2.getdata()
    new_data2 = []
    for item in data2:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data2.append((255, 255, 255, 0))
        else:
            new_data2.append(item)
    img2.putdata(new_data2)
    img2.save(f'images/txtimage-{cookie_pic_int}.png')
    return (img2, cookie_pic_int)


def open_cookie(your_fortune):
    img = Image.open("fc4.png")
    img2, cookie_pic = amorphism(fortune_builder(your_fortune), size=img.size)
    img.paste(img2, (0, 0), img2)
    img.save(f'images/combined-{cookie_pic}.png')
    args = {"cookie_image": f'combined-{cookie_pic}.png'}
    return args

def get_fortune() -> str:
    """
    This is the primary landing page for the fortune service.
    """

    possible = [
        "People are naturally attracted to you.",
        "You learn from your mistakes... You will learn a lot today.",
        "If you have something good in your life, don't let it go!",
        "Your shoes will make you happy today.",
        "You cannot love life until you live the life you love.",
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
        "Everyone agrees. You are the best.",
        "Jealousy doesn't open doors, it closes them!",
        "It's better to be alone sometimes.",
        "When fear hurts you, conquer it and defeat it!",
        "Let the deeds speak.",
        "The man on the top of the mountain did not fall there.",
        "You will conquer obstacles to achieve success.",
        "Joys are often the shadows, cast by sorrows.",
        "Fortune favors the brave.",
    ]
    your_fortune = random.choice(possible)
    return your_fortune


def fortune(request):
    my_fortune = get_fortune()
    args = {"fortune": my_fortune}
    cookie_img = open_cookie(my_fortune)
    args.update(cookie_img)
    page = Page(filename="seer.html", args=args)
    return page.render()


def register(service):
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/add/{service}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


def unregister(service):
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/remove/{service}/{LOCAL_IP}/{PORT}")
    print(r.status_code)


def main():
    print("The fortune_cookie microservice web server is starting up!")
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
