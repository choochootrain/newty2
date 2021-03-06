# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TechcrunchItem(Item):
  title = Field()
  author = Field()
  date = Field()
  text = Field()
  link = Field()
