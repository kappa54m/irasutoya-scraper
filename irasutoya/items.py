# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


#class IrasutoyaItem(scrapy.Item):
#    # define the fields for your item here like:
#    # name = scrapy.Field()
#    pass

class DictWrapperItem(Item):
    """
    Initialize item from dict.
    Set values of item as with a dict.
    """
    def __init__(self, d: dict):
        super().__init__()
        for k, v in d.items():
            self.__setitem__(k, v)

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super().__setitem__(key, value)


class IrasutoyaIrasutoListItem(DictWrapperItem):
    pass


class IrasutoyaIrasutoItem(DictWrapperItem):
    pass
