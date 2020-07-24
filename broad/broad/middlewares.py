import os


class RandomPayloadMiddleware:
    def __init__(self, size):
        self.size = size

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getint('SCRAPY_BENCH_RANDOM_PAYLOAD_SIZE'))

    def process_start_requests(self, start_requests, spider):
        for request in start_requests:
            if self.size and request.body == b'':
                yield request.replace(body=os.urandom(self.size))
            else:
                yield request
