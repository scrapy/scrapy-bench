import csv
from datetime import datetime

from scrapy import Request, Spider
from six import text_type


class CSVSpider(Spider):
    """Visits the URLs from the specified column of the specified CSV file.

    If you specify a protocol, column values are interpreted as domains, and
    the specified protocol is used for requests.
    """
    name = 'csv'

    custom_settings = {
        'CONCURRENT_REQUESTS': 100,  # https://docs.scrapy.org/en/latest/topics/broad-crawls.html#increase-concurrency
        'DUPEFILTER_DEBUG': True,
        'HTTPERROR_ALLOW_ALL': True,
        'RETRY_TIMES': 0,
    }

    def start_requests(self):
        self.response_count = 0
        self.start_time = datetime.utcnow()
        protocol = getattr(self, 'protocol', None)
        with open(self.csv_file, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                url = row[self.column]
                if protocol:
                    url = '%s://%s' % (protocol, url)
                yield Request(url)

    def parse(self, response):
        self.response_count += 1

    def close(self, reason):
        run_time = datetime.utcnow() - self.start_time
        with open("Benchmark.txt", 'w') as f:
            f.write(text_type(self.response_count / run_time.total_seconds()))
