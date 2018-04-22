import os
import sys
import time
from datetime import date

from bs4 import BeautifulSoup
import requests

# URL = "https://www3.nhk.or.jp/news/easy/?utm_int=all_header_menu_easy"
URL = "https://www3.nhk.or.jp/news/easy/news-list.json"
ARTICLE_DIR = "../material"
URL_EASY = "https://www3.nhk.or.jp/news/easy"

send_header = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6"
}

response = requests.request(method="GET", url=URL, headers=send_header)

article_today_dir = ARTICLE_DIR + "/" + str(date.today()) + "/news"
if not os.path.exists(article_today_dir):
    os.makedirs(article_today_dir)

article_list = response.json()
article_today = article_list[0].get(str(date.today()))

for article in article_today:
    article_id = str(article.get('news_id'))
    article_title = str(article.get('title'))
    article_title_with_ruby = str(article.get('title_with_ruby'))
    article_news_web_image_uri = str(article.get('news_web_image_uri'))
    article_news_web_url = URL_EASY + "/" + article_id + "/" + str(article.get('news_id')) + ".html"

    # 获取图片以及文章信息
    # try:
    #     article_img = requests.get(article_news_web_image_uri, headers=send_header).content
    #     open(article_today_dir + "/" + article_id + ".jpg", "wb").write(article_img)
    # except Exception as e:
    #     print("save article_img error", e)

    try:
        article_content_html = requests.get(article_news_web_url, headers=send_header).content
        soup = BeautifulSoup(article_content_html, "html5lib")
        article_content = str(soup.findAll(id="js-article-body")[0])
    except Exception as e:
        print("pull article content error", e)
        sys.exit(0)

    try:
        article_file = open(article_today_dir + "/" + article_id + ".html", "w+", encoding='utf-8')

        # print("start ", article_news_web_image_uri)
        article_file.writelines("<img src='" + article_news_web_image_uri + "'>")
        article_file.writelines("\n")
        article_file.writelines("\n")

        # print("start ", article_title_with_ruby)
        article_file.writelines("<div>" + article_title_with_ruby + "</div>")
        article_file.writelines("\n")
        article_file.writelines("\n")

        # print("start ", article_content)
        article_file.writelines(article_content)
        article_file.writelines("\n")
        article_file.writelines("\n")

        # print("start ", article_title)
        article_file.writelines(article_title)
        article_file.writelines("\n")
        article_file.writelines("\n")

        # print("start ", article_news_web_url)
        article_file.writelines(article_news_web_url)

        print("pass")

        article_file.close()
    except Exception as e:
        print("fatal error", e)
        sys.exit(0)

    time.sleep(5)



