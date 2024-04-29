from irasutoya.items import IrasutoyaIrasutoItem

import scrapy
from bs4 import BeautifulSoup

import csv
import os
import os.path as osp
from typing import Optional
from pathlib import Path
import functools


class IrasutoyaIrasutosSpider(scrapy.Spider):
    name = 'irasutoya__irasutos'

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set('ITEM_PIPELINES',
                     {**settings.get('ITEM_PIPELINES', {}), 'scrapy.pipelines.images.ImagesPipeline': 1})
        settings.set('IMAGES_STORE', settings['IRASUTOYA_IRASUTOS_SAVE_DIR'])

    def __init__(self, irasuto_lists_csv: Optional[str]=None):
        self.irasuto_brief_infos = []
        urls = set()
        if irasuto_lists_csv and osp.isfile(irasuto_lists_csv):
            with open(irasuto_lists_csv , encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['url'] not in urls:
                        urls.add(row['url'])
                        self.irasuto_brief_infos.append(row)
        else:
            self.logger.error("irasuto_lists_csv not provided!")

    def start_requests(self):
        reqs = []
        for i, d in enumerate(self.irasuto_brief_infos):
            reqs.append(scrapy.Request(d['url'],
                        meta={'title': d['title'], 'page_url': d['url'], 'dl_index': i}))
        return reqs

    def parse(self, response):
        doc = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        self.logger.info("Downloading [{}/{} ({:.01f}%)] '{}'".format(
            response.meta.get('dl_index', -2) + 1, len(self.irasuto_brief_infos),
            100 * (response.meta.get('dl_index', -2) + 1) / (len(self.irasuto_brief_infos)),
            response.meta.get('title', "???")))

        d = {
            'page_url': response.meta['page_url'],
        }
        main_cont = doc.select_one("#main #Blog1 #post")
        d['title'] = getattr(main_cont.select_one(".title"), 'text', '').strip()

        img_urls = []
        #sep_es = doc.select("#main #Blog1 #post > .entry > p > .separator")
        #for sep_e in sep_es:
        #    im_e = sep_e.select_one("a img")
        #    if im_e:
        #        img_urls.append(im_e.parent['href'])
        for im_e in doc.select("#main #Blog1 #post > .entry a img"):
            img_urls.append(im_e.parent['href'])
        d['image_urls'] = img_urls
        entry_es = doc.select("#main #Blog1 #post > .entry")
        assert len(entry_es) == 1
        d['entry_raw'] = str(entry_es[0])
        sep_es = doc.select("#main #Blog1 #post > .entry > p > .separator")
        d['description'] = sep_es[-1].text if len(sep_es) > 0 else None

        d['tags'] = []
        for tag_e in main_cont.select(".titlemeta .category [rel=tag]"):
            d['tags'].append(tag_e.text)

        upload_date_str = getattr(main_cont.select_one(".entry-post-date"), 'text', '').strip()
        prefix = "公開日："
        if upload_date_str.startswith(prefix):
            upload_date_str = upload_date_str[len(prefix):]
        d['upload_date'] = upload_date_str

        yield IrasutoyaIrasutoItem(d)
