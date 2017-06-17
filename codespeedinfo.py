import urllib2
import platform
import json
from datetime import datetime

import scrapy

current_date = datetime.today()


def get_latest_commit(owner, repo):
    url = 'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1'.format(
        owner=owner, repo=repo)
    response = urllib2.urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]


def get_env():
    pyimplement = platform.python_implementation()
    pyversion = platform.python_version()
    scrapyversion = '.'.join(map(str, scrapy.version_info))

    return pyimplement + " " + pyversion + " Scrapy " + scrapyversion
