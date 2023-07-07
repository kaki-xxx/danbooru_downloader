import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from itertools import count

import requests

from danbooru_downloader.scraping import (
    fetch_post_urls, fetch_image_url
)

save_dir_root = Path.home() / 'Pictures/danbooru'


def extract_file_name(url):
    """ URLからファイル名を抽出する """
    parse_result = urlparse(url)
    path = Path(parse_result.path)
    return path.name


def save_image(image_url, dst):
    """ URL先の画像をローカルに保存する """
    file_name = extract_file_name(image_url)

    # ファイル名が255文字を超えていたらファイルが作成できないので
    # 後ろ255文字分をファイル名として使う
    if len(file_name) > 255:
        file_name = file_name[-255:]

    # すでにファイルが存在する場合なにもしない
    if (dst / file_name).exists():
        return

    # 画像ファイルのバイナリデータを取得
    r = requests.get(image_url)
    image_resource = r.content

    with open(dst / file_name, mode='wb') as f:
        print(f'{file_name}を保存')
        f.write(image_resource)


def main(search_tags):
    # もし保存するためのディレクトリが存在しない場合作成する
    if not save_dir_root.exists():
        os.makedirs(save_dir_root)
    save_dir = save_dir_root / '+'.join(search_tags)
    if not save_dir.exists():
        os.makedirs(save_dir)

    payload = {'utf-8': '✓', 'tags': ' '.join(sys.argv[1:])}
    r = requests.get('https://danbooru.donmai.us/posts', params=payload)
    print(r.url)

    base_url = 'https://danbooru.donmai.us/'
    for i in count(1):
        print(f'{i}ページ目')
        post_urls = fetch_post_urls(r.url, str(i))
        if post_urls is None:
            print('最後のページに到達しました')
            break
        for post_url in post_urls:
            abs_url = urljoin(base_url, post_url)
            image_url = fetch_image_url(abs_url)
            save_image(image_url, save_dir)
