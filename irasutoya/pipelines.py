# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from irasutoya import db
from irasutoya.utils import list_to_csv
from irasutoya.items import IrasutoyaIrasutoListItem, IrasutoyaIrasutoItem

from itemadapter import ItemAdapter

import datetime
import json


class IrasutoyaPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.use_db = bool(settings['USE_DB'])
        if self.use_db:
            self.db_engine = db.get_db_engine()
            self.Session = db.sessionmaker(bind=self.db_engine)
        else:
            self.db_engine = None
            self.Session = None

    def process_item(self, item, spider):
        if self.use_db:
            with self.Session() as sess:
                entry = None
                if isinstance(item, IrasutoyaIrasutoListItem):
                    spider.logger.warning("TODO db pipeline note implemented for IrasutoyaIrasutoListItem")
                elif isinstance(item, IrasutoyaIrasutoItem):
                    entry = self.__process_irasutoya_irasuto_item(item)

                if entry is not None:
                    spider.logger.info("%s: inserting entry for %s item: %s",
                                       self.__class__, type(item), item)
                    try:
                        sess.add(entry)
                        sess.commit()
                    except:
                        sess.rollback()
                        raise
        return item

    def __process_irasutoya_irasuto_item(self, item):
        entry = db.IrasutoyaIrasuto()
        entry.title = item['title']
        entry.description = item['description']
        entry.entry_raw = item['entry_raw']
        entry.tags = list_to_csv(item['tags'])
        entry.upload_date = item['upload_date']
        entry.images_download_info = json.dumps(item['images'])
        entry.scraped_datetime = datetime.datetime.now()
        return entry
