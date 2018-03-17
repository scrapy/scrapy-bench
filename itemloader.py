from timeit import default_timer as timer
import tarfile

import scrapy
import click
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse


class ItemloaderItem(scrapy.Item):
    rating = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


def main():
    total = 0
    time = 0
    tar = tarfile.open("bookfiles.tar.gz")

    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()
        response = HtmlResponse(url="local", body=html, encoding='utf8')

        for i in xrange(0, 10):
            start = timer()
            loader = ItemLoader(item=ItemloaderItem(), response=response)
            loader.add_xpath(
                'rating', '//*[@id="content_inner"]/article/div[1]/div[2]/p[3]/i[1]')
            loader.add_xpath(
                'title', '//*[@id=("content_inner")]/article/div[1]/div[2]/h1')
            loader.add_xpath(
                'price', '//*[@id=("content_inner")]/article/div[1]/div[2]/p[1]')
            loader.add_css('stock', '.product_main .instock.availability ::text')
            loader.add_css('category', 'ul.breadcrumb li:nth-last-child(2) ::text')
            loader.add_value('name', 'item {}'.format(i))
            loader.add_value('url', 'http://site.com/item{}'.format(i))
            product = loader.load_item()
            end = timer()

            total += 1
            time = time + end - start


    print("\nTotal number of items extracted = {0}".format(total))
    print("Time taken = {0}".format(time))
    click.secho("Rate of link extraction : {0} items/second\n".format(
        float(total / time)), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
