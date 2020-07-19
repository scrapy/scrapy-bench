import os


class RandomPayloadMiddleware:
    def __init__(self, size):
        self.size = size

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getint('SCRAPY_BENCH_RANDOM_PAYLOAD_SIZE'))

    def process_request(self, request, spider):
        if not self.size or request.body != b'':
            return

        return request.replace(body=os.urandom(self.size))
