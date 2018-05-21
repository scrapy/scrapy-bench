from timeit import default_timer as timer
import tarfile

import scrapy
import click
import six
from w3lib.url import (parse_data_uri, file_uri_to_path, safe_url_string,
                       canonicalize_url, any_to_uri)
from scrapy.http import HtmlResponse


def main():

    from profilehooks import profile
    urlparseprofile_name = "urlparseprofile.prof"

    @profile(filename=urlparseprofile_name)
    def profilehooks_profling():
        total = 0
        time = 0
        time_file_uri_to_path = 0
        time_safe_url_string = 0
        time_canonicalize_url = 0

        tar = tarfile.open("sites.tar.gz")
        urls = []

        for member in tar.getmembers():
            f = tar.extractfile(member)
            html = f.read()
            response = HtmlResponse(url="local", body=html, encoding='utf8')

            links = response.css('a::attr(href)').extract()
            urls.extend(links)

        for url in urls:
            start_file_uri_to_path = timer()
            file_uri_to_path(url)
            end_file_uri_to_path = timer()
            time_file_uri_to_path += (end_file_uri_to_path - start_file_uri_to_path)
            time += (end_file_uri_to_path - start_file_uri_to_path)

            start_safe_url_string = timer()
            safe_url_string(url)
            end_safe_url_string = timer()
            time_safe_url_string += (end_safe_url_string - start_safe_url_string)
            time += (end_safe_url_string - start_safe_url_string)

            start_canonicalize_url = timer()
            canonicalize_url(url)
            end_canonicalize_url = timer()
            time_canonicalize_url += (end_canonicalize_url - start_canonicalize_url)
            time += (end_canonicalize_url - start_canonicalize_url)

            # any_to_uri(url) # Error on Python 2: KeyError: u'\u9996'

            total += 1

        print("\nTotal number of items extracted = {0}".format(total))
        print("Time spent on file_uri_to_path = {0}".format(time_file_uri_to_path))
        print("Time spent on safe_url_string = {0}".format(time_safe_url_string))
        print("Time spent on canonicalize_url = {0}".format(time_canonicalize_url))
        print("Total time taken = {0}".format(time))
        click.secho("Rate of link extraction : {0} items/second\n".format(
            float(total / time)), bold=True)

        with open("Benchmark.txt", 'w') as g:
            g.write(" {0}".format((float(total / time))))

    profilehooks_profling()


if __name__ == "__main__":
    main()
