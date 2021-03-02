#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
from timeit import default_timer as timer
import io
import tarfile

import click
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse, TextResponse
from six.moves.urllib.parse import urlparse


def main():
    url = 'https://scrapy.org/'
    link_extractor = LinkExtractor()
    total = 0
    time = 0
    tar = tarfile.open("sites.tar.gz")
    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()

        start = timer()

        response = HtmlResponse(url=url, body=html, encoding='utf8')
        links = link_extractor.extract_links(response)

        end = timer()

        total = total + len(links)
        time = time + end - start

    print("\nTotal number of links extracted = {0}".format(total))
    print("Time taken = {0}".format(time))
    click.secho("Rate of link extraction : {0} links/second\n".format(
        float(total / time)), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
