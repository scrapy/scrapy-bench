from timeit import default_timer as timer
import datetime

import scrapy
import click
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse


class ItemloaderItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


# def main():
#     total = 30000
#     time = 0
#
#     products = []
#     for i in xrange(0, 30000):
#         start = timer()
#         response = HtmlResponse(url='http://example/com/')
#         loader = ItemLoader(item=ItemloaderItem(), response=response)
#         loader.add_value('name', 'item {}'.format(i))
#         loader.add_value('url', 'http://site.com/item{}'.format(i))
#
#         product = loader.load_item()
#         products.append(product)
#         end = timer()
#         time = time + end - start
#
#
#     print("\nTotal number of items extracted = {0}".format(total))
#     print("Time taken = {0}".format(time))
#     click.secho("Rate of link extraction : {0} items/second\n".format(
#         float(60 * total / time)), bold=True)
#
#     with open("Benchmark.txt", 'w') as g:
#         g.write(" {0}".format((60 * float(total / time))))
#
#
# if __name__ == "__main__":
#     main()


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
        print(self.timesec)

    def close(self, reason):
        with open("Benchmark.txt", 'w') as f:
            f.write(" {0}".format(
                (self.items * (60 / self.timesec.total_seconds()))))
        click.secho("\nThe average speed of the spider is {0} items/min\n".format(
            self.items * (60 / self.timesec.total_seconds())), bold=True)

default_settings = {
    'LOG_LEVEL': 'INFO',
    'LOGSTATS_INTERVAL': 1
}

process = CrawlerProcess(default_settings)

process.crawl(ItemLoaderSpeed)
process.start()
