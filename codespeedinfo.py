import urllib2
import urllib
import platform
import json
from datetime import datetime

import scrapy
import statistics

current_date = datetime.today()
CODESPEED_URL = 'http://localhost:8000/'


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


def uploadresult(test, w):
    commit = get_latest_commit('scrapy', 'scrapy')

    data = {
        'commitid': commit['html_url'].rsplit('/', 1)[-1],
        'branch': 'default',  # Always use default for trunk/master/tip
        'project': 'Scrapy-Bench',
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
    params = urllib.urlencode(data)
    response = "None"
    print("Saving result for executable %s, revision %s, benchmark %s" % (
        data['executable'], data['commitid'], data['benchmark']))
    try:
        f = urllib2.urlopen(CODESPEED_URL + 'result/add/', params)
    except urllib2.HTTPError as e:
        print(str(e))
        print(e.read())
        return
    response = f.read()
    f.close()
    print("Server (%s) response: %s\n" % (CODESPEED_URL, response))
