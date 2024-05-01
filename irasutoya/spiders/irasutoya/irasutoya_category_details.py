import scrapy
from bs4 import BeautifulSoup
import requests

import json
import os
import os.path as osp
from pathlib import Path
from urllib.parse import urljoin


class IrasutoyaShosaiCategoriesSpider(scrapy.Spider):
    name = 'irasutoya__category_details'

    start_urls = ["https://www.irasutoya.com/"]

    def __init__(self, json_save_path):
        self.json_save_path = Path(json_save_path)
        if self.json_save_path.suffix != '.json' or self.json_save_path.is_dir():
            raise ValueError("Invalid json_save_path")
        self.json_save_path.parent.mkdir(parents=True, exist_ok=True)

    def parse(self, response):
        doc = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        cont = doc.select_one("#wrapper #content #homedesign #section_banner")
        categories = []
        for a in cont.select(":scope > a"):
            cate_tag = a.select_one("img")['alt']
            cate_url = a['href']
            if cate_url == "https://www.irasutoya.com/2021/01/onepiece.html":
                self.logger.info("Skipping One Piece ({}; {})".format(cate_url, cate_tag))
                continue

            if not cate_url.startswith("/p/") and cate_url.endswith(".html"):
                raise AssertionError("Unexpected top level category ({}) url: '{}'".format(cate_tag, cate_url))

            cate_url = urljoin(response.url, cate_url)
            self.logger.info("Found category: '{}' ({})".format(cate_tag, cate_url))
            categories.append({
                'tag': cate_tag,
                'url': cate_url,
            })

        subcategories = []
        for icate, cate in enumerate(categories):
            self.logger.info("[{}/{}] Parsing top level category '{}'".format(icate+1, len(categories), cate['tag']))
            doc2 = BeautifulSoup(requests.get(cate['url']).content.decode('utf-8'), 'html.parser')
            cont = doc2.select_one("#wrapper #main #post")
            cate_tag = cont.select_one(".title").text.strip()
            entry_e = cont.select_one(".entry")
            cate_desc = entry_e.select_one(":scope > p").text
            cate['title'] = cate_tag
            cate['description'] = cate_desc

            cate2_tag = None
            for ch_e in cont.select_one("#banners").find_all(recursive=False):
                if ch_e.name == 'h3':
                    cate2_tag = ch_e.text.strip()
                    #print("== cate2: '{}'".format(cate2_tag))
                elif ch_e.name == 'a':
                    subcate_url = ch_e['href']
                    subcate_tag = ch_e.select_one("img").get('alt', None)
                    subcategories.append({
                        'category1_tag': cate['tag'],
                        'category1_url': cate['url'],
                        'category2_tag': cate2_tag,
                        'tag': subcate_tag,
                        'url': subcate_url,
                    })
                    #print("{} ({})".format(subcate_tag, subcate_url))
            #print()

        self.logger.info("#categories: %d, #subcategories: %d", len(categories), len(subcategories))
        with open(self.json_save_path, 'w', encoding='utf-8') as f:
            d = {
                'categories': categories,
                'subcategories': subcategories,
            }
            json.dump(d, f, ensure_ascii=False)
        self.logger.info("Saved results to '%s'.", self.json_save_path)
