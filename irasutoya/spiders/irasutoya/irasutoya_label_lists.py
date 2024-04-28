from irasutoya.items import IrasutoyaIrasutoListItem

import scrapy
from bs4 import BeautifulSoup

import csv
from typing import Optional, List
import os
import os.path as osp
from pathlib import Path
import re


class IrasutoyaLabelListsSpider(scrapy.Spider):
    name = 'irasutoya__label_lists'

    def __init__(self, shosai_categories_csv: Optional[str]=None):
        self.categories = []
        if shosai_categories_csv and osp.isfile(shosai_categories_csv):
            with open(shosai_categories_csv, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.categories.append(row)
        else:
            self.logger.error("shosai_categories_csv not provided!")

    def start_requests(self):
        reqs = []
        for cate_d in self.categories:
            reqs.append(scrapy.Request(cate_d['url'],
                                       meta={'label': cate_d['name'], 'page': 0}))
        return reqs

    def parse(self, response):
        self.logger.debug("'%s' page %d", response.meta.get('label'),
                          response.meta.get('page'))
        doc = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        contents = doc.select("#post")
        self.logger.info("#content=%d", len(contents))
        for ic, c in enumerate(contents):
            d = {}
            a = c.select_one(".boxmeta > h2 > a")
            d['title'] = getattr(a, 'text', "")
            d['url'] = a['href']
            # grab thumbnail (small size)
            boxim = str(c.select_one(".boxim"))
            m = re.search(r"document\.write\(bp_thumbnail_resize\(\"(.+)\",", boxim)
            if m:
                d['thumb_url'] = m.group(1)
            else:
                self.logger.error("Could not find thumbnail url (boxim=%s)", boxim)
                d['thumb_url'] = None
            d['shosai_category'] = response.meta['label']

            yield IrasutoyaIrasutoListItem(d)

        # Pagination
        nav_e = doc.select_one("#navigation #blog-pager")
        next_pg_es = nav_e.select("#blog-pager-older-link a.blog-pager-older-link")
        if len(next_pg_es) == 0:
            home_e = nav_e.select_one("#home-link .home-link .navibtn")
            assert home_e is not None
            self.logger.info("Last page")
        else:
            assert len(next_pg_es) == 1
            #self.logger.debug("len(next_pg_es)=%d", len(next_pg_es))
            next_pg_e = next_pg_es[0]
            im_e = next_pg_e.select_one(":scope > img[alt]")
            if im_e['alt'] == "次のページ":
                next_pg_url = next_pg_e['href']
                yield response.follow(next_pg_url,
                                      meta={'label': response.meta['label'],
                                            'page': response.meta['page'] + 1})
