import scrapy
from scrapy.loader import ItemLoader

from itemloader.items import ItemloaderItem


class ItemLoaderSpeed(scrapy.Spider):
    name = 'itemloaderspider'

    def __init__(self, **kw):
        super(BroadBenchSpider, self).__init__(**kw)

        self.items = 0

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/')

    def parse(self, response):
        for i in xrange(0, 30000):
            loader = ItemLoader(item=ItemloaderItem(), response=response)
            loader.add_value('name', 'item {}'.format(i))
            loader.add_value('url', 'http://site.com/item{}'.format(i))

            product = loader.load_item()
            print self.crawler.stats.get_value('item_scraped_count', 0)
            yield product
