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


try:
    from local_settings import *
except ImportError:
    pass
