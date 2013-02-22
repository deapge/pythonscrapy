# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ItunesItem(Item):
    # define the fields for your item here like:
    # name = Field()
    image = Field()
    stars = Field()
    title = Field()
    category = Field()
    desc = Field()
    link = Field()
    pass
