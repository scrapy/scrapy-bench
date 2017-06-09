#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import io
from timeit import default_timer as timer
import tarfile

from scrapy.http import HtmlResponse, TextResponse, Response, request
import click


def main():
    total = 0
    time = 0
    tar = tarfile.open("bookfiles.tar.gz")
    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()

        response = HtmlResponse(url="local", body=html, encoding='utf8')

        start = timer()

        rating = response.css(
            'p.star-rating::attr(class)').extract_first().split(' ')[-1]
        title = response.css('.product_main h1::text').extract_first()
        price = response.css(
            '.product_main p.price_color::text').re_first('£(.*)')
        stock = ''.join(
            response.css('.product_main .instock.availability ::text').re('(\d+)'))
        category = ''.join(
            response.css('ul.breadcrumb li:nth-last-child(2) ::text').extract()).strip()

        end = timer()
        page = [rating, title, price, stock, category]

        total = total + 1
        time = time + end - start

    print("\nTotal number of pages extracted = {0}".format(total))
    print("Time taken = {0}".format(time))
    click.secho("Rate of link extraction : {0} pages/second\n".format(
        float(total / time)), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
