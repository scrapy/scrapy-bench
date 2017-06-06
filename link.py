#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
from timeit import default_timer as timer
import io

import click
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse, TextResponse, Response
from six.moves.urllib.parse import urlparse


def main():
    start = timer()

    url = 'http://scrapinghub.com/'
    link_extractor = LinkExtractor()
    total = 0
    for files in glob.glob('sites/*'):

        f = (io.open(files, "r", encoding="utf-8"))
        html = f.read()

        r3 = HtmlResponse(url=url, body=html, encoding='utf8')
        links = link_extractor.extract_links(r3)
        total = total + len(links)
    end = timer()
    print("\nTotal number of links extracted = {0}".format(total))
    print("Time taken = {0}".format(end - start))
    click.secho("Rate of link extraction : {0} links/second\n".format(
        float(total / (end - start))), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / (end - start)))))


if __name__ == "__main__":
    main()
