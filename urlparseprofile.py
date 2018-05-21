from timeit import default_timer as timer
import tarfile

import scrapy
import click
import six
from six.moves.urllib.parse import (urljoin, urlsplit, urlunsplit,
                                    urldefrag, urlencode, urlparse,
                                    quote, parse_qs, parse_qsl,
                                    ParseResult, unquote, urlunparse)
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse


def urljoin_profile(base, ref):
    return urljoin(base, ref)


def main():
    total = 0
    time = 0
    tar = tarfile.open("sites.tar.gz")

    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()
        response = HtmlResponse(url="local", body=html, encoding='utf8')

        urls = response.css('a::attr(href)').extract()


        print(urls)

    # print("\nTotal number of items extracted = {0}".format(total))
    # print("Time taken = {0}".format(time))
    # click.secho("Rate of link extraction : {0} items/second\n".format(
    #     float(total / time)), bold=True)
    #
    # with open("Benchmark.txt", 'w') as g:
    #     g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
