from timeit import default_timer as timer
import tarfile

import scrapy
import click
import six
from w3lib.url import (parse_data_uri, file_uri_to_path, safe_url_string,
                       canonicalize_url, any_to_uri)
from scrapy.http import HtmlResponse


def urljoin_profile(base, ref):
    return urljoin(base, ref)


def main():
    total = 0
    time = 0
    tar = tarfile.open("sites.tar.gz")
    urls = []

    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()
        response = HtmlResponse(url="local", body=html, encoding='utf8')

        links = response.css('a::attr(href)').extract()
        urls.extend(links)

    for url in urls:
        start = timer()

        file_uri_to_path(url)
        safe_url_string(url)
        canonicalize_url(url)
        # any_to_uri(url) Error on Python 2: KeyError: u'\u9996'

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
