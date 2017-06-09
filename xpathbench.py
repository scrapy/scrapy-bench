#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import io
from timeit import default_timer as timer

from scrapy.http import HtmlResponse, TextResponse, Response, request
import click


def main():
    start = timer()
    total = 0

    for files in glob.glob('bookfile/*'):
        f = (io.open(files, "r", encoding="utf-8"))
        html = f.read()

        response = HtmlResponse(url="local", body=html, encoding='utf8')
        rating = response.css(
            'p.star-rating::attr(class)').extract_first().split(' ')[-1]
        title = response.css('.product_main h1::text').extract_first()
        price = response.css(
            '.product_main p.price_color::text').re_first('£(.*)')
        stock = ''.join(
            response.css('.product_main .instock.availability ::text').re('(\d+)'))
        category = ''.join(
            response.css('ul.breadcrumb li:nth-last-child(2) ::text').extract()).strip()
        page = [rating, title, price, stock, category]
        total = total + 1
    end = timer()
    print("\nTotal number of pages extracted = {0}".format(total))
    print("Time taken = {0}".format(end - start))
    click.secho("Rate of link extraction : {0} pages/second\n".format(
        float(total / (end - start))), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / (end - start)))))


if __name__ == "__main__":
    main()
