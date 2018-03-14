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


def main():
    total = 30000
    time = 0
    response = HtmlResponse(url='http://example/com/')
    products = []
    for i in xrange(0, 30000):
        start = timer()
        loader = ItemLoader(item=ItemloaderItem(), response=response)
        loader.add_value('name', 'item {}'.format(i))
        loader.add_value('url', 'http://site.com/item{}'.format(i))

        product = loader.load_item()
        products.append(product)
        end = timer()
        time = time + end - start


    print("\nTotal number of items extracted = {0}".format(total))
    print("Time taken = {0}".format(time))
    click.secho("Rate of link extraction : {0} items/second\n".format(
        float(total / time)), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
