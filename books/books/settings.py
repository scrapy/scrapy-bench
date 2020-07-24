from __future__ import absolute_import

BOT_NAME = 'books'

SPIDER_MODULES = ['books.spiders']
NEWSPIDER_MODULE = 'books.spiders'

CLOSESPIDER_ITEMCOUNT = 1000
RETRY_ENABLED = False
COOKIES_ENABLED = True

LOGSTATS_INTERVAL = 3
LOG_LEVEL = 'INFO'
MEMDEBUG_ENABLED = True
CONCURRENT_REQUESTS = 120

SCRAPY_BENCH_RANDOM_PAYLOAD_SIZE = None

SPIDER_MIDDLEWARES = {
    'books.middlewares.RandomPayloadMiddleware': 1000,
}

try:
    from .local_settings import *
except ImportError:
    pass
