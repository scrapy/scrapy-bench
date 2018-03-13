import datetime

import scrapy
import click
from scrapy.loader import ItemLoader

from itemloader.items import ItemloaderItem


class ItemLoaderSpeed(scrapy.Spider):
    name = 'itemloaderspider'

    def __init__(self, **kw):
        super(ItemLoaderSpeed, self).__init__(**kw)

        self.items = 0
        self.timesec = datetime.datetime.utcnow()

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/')

    def parse(self, response):
        for i in xrange(0, 30000):
            loader = ItemLoader(item=ItemloaderItem(), response=response)
            loader.add_value('name', 'item {}'.format(i))
            loader.add_value('url', 'http://site.com/item{}'.format(i))

            product = loader.load_item()

            yield product

        self.items = self.crawler.stats.get_value('item_scraped_count', 0)
        a = self.crawler.stats.get_value('start_time')
        b = datetime.datetime.utcnow()
        self.timesec = b - a

    def close(self, reason):
        with open("Benchmark.txt", 'w') as f:
            f.write(" {0}".format(
                (self.items * (60 / self.timesec.total_seconds()))))
        click.secho("\nThe average speed of the spider is {0} items/min\n".format(
            self.items * (60 / self.timesec.total_seconds())), bold=True)
