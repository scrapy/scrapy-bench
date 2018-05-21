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


def urljoin_rfc(base, ref, encoding='utf-8'):
    r"""
    .. warning::

        This function is deprecated and will be removed in future.
        It is not supported with Python 3.
        Please use ``urlparse.urljoin`` instead.

    Same as urlparse.urljoin but supports unicode values in base and ref
    parameters (in which case they will be converted to str using the given
    encoding).

    Always returns a str.

    >>> import w3lib.url
    >>> w3lib.url.urljoin_rfc('http://www.example.com/path/index.html', u'/otherpath/index2.html')
    'http://www.example.com/otherpath/index2.html'
    >>>

    >>> # Note: the following does not work in Python 3
    >>> w3lib.url.urljoin_rfc(b'http://www.example.com/path/index.html', u'fran\u00e7ais/d\u00e9part.htm') # doctest: +SKIP
    'http://www.example.com/path/fran\xc3\xa7ais/d\xc3\xa9part.htm'
    >>>


    """

    warnings.warn("w3lib.url.urljoin_rfc is deprecated, use urlparse.urljoin instead",
        DeprecationWarning)

    str_base = to_bytes(base, encoding)
    str_ref = to_bytes(ref, encoding)
    return urljoin(str_base, str_ref)
    

def main():
    total = 0
    time = 0
    tar = tarfile.open("bookfiles.tar.gz")

    for member in tar.getmembers():
        f = tar.extractfile(member)
        html = f.read()
        response = HtmlResponse(url="local", body=html, encoding='utf8')






    print("\nTotal number of items extracted = {0}".format(total))
    print("Time taken = {0}".format(time))
    click.secho("Rate of link extraction : {0} items/second\n".format(
        float(total / time)), bold=True)

    with open("Benchmark.txt", 'w') as g:
        g.write(" {0}".format((float(total / time))))


if __name__ == "__main__":
    main()
