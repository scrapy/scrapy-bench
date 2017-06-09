#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import scrapy
from scrapy.http import TextResponse

i = 1

reload(sys)
sys.setdefaultencoding('utf-8')


class TestSpider(scrapy.Spider):
    name = "downloader"
    start_urls = [
        # Enter the site urls here
    ]

    def parse(self, TextResponse):
        global i
        filename = str(i) + '.html'
        with open("foldername/" + filename, 'w') as f:
            f.write(TextResponse.text)
        i = i + 1
