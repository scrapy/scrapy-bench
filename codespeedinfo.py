import platform
import re
from datetime import datetime

import requests
import scrapy
import statistics

current_date = datetime.today()
CODESPEED_URL = 'http://localhost:8000/'


def get_latest_commit(owner, repo):
    url = ('https://api.github.com/repos/{owner}/{repo}/commits?per_page=1'
           .format(owner=owner, repo=repo))
    return requests.get(url).json()[0]


def get_env():
    pyimplement = platform.python_implementation()
    pyversion = platform.python_version()
    scrapyversion = '.'.join(map(str, scrapy.version_info))
    return '{} {} Scrapy {}'.format(pyimplement, pyversion, scrapyversion)


def uploadresult(test, w):
    commit = get_latest_commit('scrapy', 'scrapy')
    data = {
        'commitid': commit['html_url'].rsplit('/', 1)[-1],
        'branch': 'default',  # Always use default for trunk/master/tip
        'project': 'scrapy',
        'executable': 'bench.py',
        'benchmark': test,
        'environment': get_env(),
        'result_value': statistics.mean(w),
    }

    data.update({
        'revision_date': current_date,  # Optional. Default is taken either
        # from VCS integration or from current date
        'result_date': current_date,  # Optional, default is current date
        'std_dev': statistics.pstdev(w),  # Optional. Default is blank
        #'max': 4001.6,  # Optional. Default is blank
        #'min': 3995.1,  # Optional. Default is blank
    })

    print('Saving result for executable {executable}, revision {commitid}, '
          'benchmark {benchmark}'.format(**data))
    response = requests.post(CODESPEED_URL + 'result/add/', data=data)
    if not response.ok:
        print('Error uploading results: {} {}'.format(response, response.text))
    else:
        print('Results uploaded: {} {}'.format(response, response.text))
