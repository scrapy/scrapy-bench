from datetime import datetime

from scrapy import Request, Spider
from six import text_type


class HTTPSpider(Spider):
    """Spider equivalent to https://http1.golang.org/gophertiles

    Use the DOWNLOAD_HANDLERS setting to set the download handler to test.
    """
    name = 'httpbench'

    def start_requests(self):
        self.response_count = 0
        self.start_time = datetime.utcnow()
        version = (
            '2' if '2' in self.settings.getwithbase('DOWNLOAD_HANDLERS')['https']
            else '1'
        )
        for x in range(14):
            for y in range(11):
                yield Request(
                    'https://http{version}.golang.org/gophertiles?x={x}&y={y}&latency=0'
                    .format(
                        version=version,
                        x=x,
                        y=y,
                    )
                )

    def parse(self, response):
        self.response_count += 1

    def close(self, reason):
        run_time = datetime.utcnow() - self.start_time
        with open("Benchmark.txt", 'w') as f:
            f.write(text_type(self.response_count / run_time.total_seconds()))
