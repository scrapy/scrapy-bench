import os

from scrapy import Request


class RandomPayloadMiddleware:
    def __init__(self, size):
        """
        Add a random payload to test network effects

        :param name: size of payload added in bytes
        :type name: int

        """
        self.size = size

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getint('SCRAPY_BENCH_RANDOM_PAYLOAD_SIZE'))

    def handle_request(self, smth):
        if not isinstance(smth, Request):
            return smth

        request = smth

        if self.size == 0:
            return request

        request.meta['random_payload'] = os.urandom(self.size)
        return request


    def process_start_requests(self, start_requests, spider):
        for request in start_requests:
            yield self.handle_request(request)

    def process_spider_output(self, response, result, spider):
        for smth in result:
            yield self.handle_request(smth)
