import os
import time

from bs4 import BeautifulSoup
import requests


if not os.path.exists("../material"):
    os.mkdir("../material")

NAME_JAP = "1207"

ORIGIN = "http://hukumusume.com/douwa/book"
URL_WORLD = "http://hukumusume.com/douwa/book/world/wm02.html"
URL_JAP = "http://hukumusume.com/douwa/book/jap/" + NAME_JAP + ".html"
FILE = "../material/" + NAME_JAP + "/"
DIR = "../material/" + NAME_JAP

if not os.path.exists(DIR):
    os.mkdir(DIR)

URL = URL_JAP

send_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6"
}

response = requests.request(method="GET", url=URL, headers=send_header)
html = response.content

soup = BeautifulSoup(html, "html5lib")
for tag in soup.findAll(class_="bb-item"):
    for c in tag.children:
        src = str(c).replace("\"/>", "").split("..")[-1]
        img = requests.get(ORIGIN + src)
        if img.status_code == 200:
            time.sleep(1)
            open(FILE + src.split("/")[-1], 'wb').write(img.content)
            print("processing")
