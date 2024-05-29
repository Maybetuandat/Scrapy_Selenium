# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class CrawlFacebookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    idUser = scrapy.Field()
    time = scrapy.Field()
    react = scrapy.Field()
class CrawlFacebookReactItem(scrapy.Item):
    idUser = scrapy.Field()
    
    

