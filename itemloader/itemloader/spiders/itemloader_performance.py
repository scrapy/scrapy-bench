import scrapy
from scrapy.loader import ItemLoader

from itemloader.items import ItemloaderItem


class ItemLoaderSpeed(scrapy.Spider):
    name = 'itemloaderspider'

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/')

    def parse(self, response):
        for i in xrange(0, 30000):
            loader = ItemLoader(item=ItemloaderItem(), response=response)
            loader.add_value('name', 'item {}'.format(i))
            loader.add_value('url', 'http://site.com/item{}'.format(i))

            product = loader.load_item()

            yield product
