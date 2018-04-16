import os
import time
from datetime import date

from bs4 import BeautifulSoup
import requests


# Setting
ARTICLE_NAME_JAP = "1207"
ARTICLE_NAME_WORLD = ""

ARTICLE_NAME = "JAP"
URL = "JAP"


# DO NOT MODIFY

send_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6"
}

if ARTICLE_NAME == "JAP":
    ARTICLE_NAME = ARTICLE_NAME_JAP
elif ARTICLE_NAME == "WORLD":
    ARTICLE_NAME = ARTICLE_NAME_WORLD

ORIGIN = "http://hukumusume.com/douwa/book"
URL_WORLD = "http://hukumusume.com/douwa/book/world/" + ARTICLE_NAME + ".html"
URL_JAP = "http://hukumusume.com/douwa/book/jap/" + ARTICLE_NAME + ".html"
FILE = "../material/" + ARTICLE_NAME + "/"
ARTICLE_DIR = "../material"

article_today_dir = ARTICLE_DIR + "/" + str(date.today())
if not os.path.exists(article_today_dir):
    os.makedirs(article_today_dir)

if URL == "JAP":
    URL = URL_JAP
elif URL == "WORLD":
    URL = URL_WORLD

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
