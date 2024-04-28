import scrapy
from bs4 import BeautifulSoup


class IrasutoyaShosaiCategoriesSpider(scrapy.Spider):
    name = 'irasutoya__shosai_categories'

    start_urls = ["https://www.irasutoya.com/"]

    def parse(self, response):
        doc = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        cont = doc.select_one("#sidebar-wrapper #sidebar #Label1")
        if getattr(cont.select_one(":scope > h2"), 'text') != "詳細カテゴリー":
            raise ValueError("詳細カテゴリー header not found")

        shousai_cates = []
        for i, e in enumerate(cont.select(":scope > .widget-content.list-label-widget-content > ul > li")):
            a = e.select_one(":scope > a")
            if not a or a.attrs.get('dir') != 'ltr':
                raise ValueError("Unexpected list item: '{}'".format(e))
            url = a['href']
            scate = a.text

            yield {
                'name': scate,
                'url': url,
            }

