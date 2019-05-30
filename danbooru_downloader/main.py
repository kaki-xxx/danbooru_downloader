#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" danbooru.donmai.usから画像を自動で落とすダウンローダ.

Webスクレイピングによって実装しているためサイトの仕様が変わったら動かなくなる.
"""

import sys

from danbooru_downloader import download


def main():
    search_tags = sys.argv[1:]
    download.main(search_tags)


if __name__ == '__main__':
    main()
