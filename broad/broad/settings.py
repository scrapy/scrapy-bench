BOT_NAME = 'broad'

SPIDER_MODULES = ['broad.spiders']
NEWSPIDER_MODULE = 'broad.spiders'

CLOSESPIDER_ITEMCOUNT = 100000
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
