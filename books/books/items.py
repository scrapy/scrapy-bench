import scrapy


class Page(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    size = scrapy.Field()
    referer = scrapy.Field()
    newcookies = scrapy.Field()
    body = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    stock = scrapy.Field()
