from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def fetch_post_urls(base_url, page_num):
    """ サムネイルの並んだページからpostのurlをすべて返すようなイテレータを作成 """
    r = requests.get(base_url, params={'page': page_num})
    soup = BeautifulSoup(r.text, features='lxml')

    articles = soup.select('.posts-container > article')
    if len(articles) == 0:
        yield None
    for article in articles:
        a = article.select('a')
        yield a[0]['href']


def fetch_image_url(post_url):
    """ postのページから画像のurlを取得して返す """
    r = requests.get(post_url)
    soup = BeautifulSoup(r.text, features='lxml')

    resize_link = soup.select('a#image-resize-link')
    if len(resize_link) != 0:
        return resize_link[0]['href']
    else:
        image = soup.select('#image')[0]
        return image['src']
