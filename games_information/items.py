# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GamesInformationItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
    category = scrapy.Field()
    reviews_score_and_quan = scrapy.Field()
    score = scrapy.Field()



