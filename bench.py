import subprocess
import os
import sys
import urllib
import urllib2

import click
import statistics

import codespeedinfo

CODESPEED_URL = 'http://localhost:8000/'


def calculator(
        test,
        arg,
        n_runs,
        only_result,
        web=False,
        workpath=os.getcwd()):
    w = []
    for x in range(n_runs):
        if only_result:
            process = subprocess.Popen(
                arg,
                cwd=workpath,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            process.wait()
        else:
            process = subprocess.Popen(arg, cwd=workpath, shell=True)
            process.wait()
        with open(os.path.join(workpath, "Benchmark.txt")) as f:
            for line in f.readlines():
                w.append(float(line))

    click.secho(
        "\nThe results of the benchmark are (all speeds in items/sec) : \n",
        bold=True)
    click.secho(
        "\nTest = '{0}' Iterations = '{1}'\n".format(test, n_runs),
        bold=True)
    click.secho(
        "\nMean : {0} Median : {1} Std Dev : {2}\n".format(
            statistics.mean(w),
            statistics.median(w),
            statistics.pstdev(w)),
        bold=True)

    if web is True:
        commit = codespeedinfo.get_latest_commit('Parth-Vader', 'scrapy-bench')

        data = {
            'commitid': commit['html_url'].rsplit('/', 1)[-1],
            'branch': 'default',  # Always use default for trunk/master/tip
            'project': 'Scrapy-Bench',
            'executable': 'bench.py',
            'benchmark': test,
            'environment': codespeedinfo.get_env(),
            'result_value': statistics.mean(w),
        }

        data.update({
            'revision_date': codespeedinfo.current_date,  # Optional. Default is taken either
            # from VCS integration or from current date
            'result_date': codespeedinfo.current_date,  # Optional, default is current date
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

    os.remove(os.path.join(workpath, "Benchmark.txt"))


@click.group()
def cli():
    """A benchmark suite for Scrapy."""
    pass


@cli.command()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark.")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option('--uploadresult', is_flag=True, help="Upload the results")
def bookworm(n_runs, only_result, uploadresult):
    """Spider to scrape locally hosted site"""
    workpath = os.path.join(os.getcwd(), "books")
    arg = "scrapy crawl followall -o items.csv"
    calculator("Book Spider", arg, n_runs, only_result, uploadresult, workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option('--uploadresult', is_flag=True, help="Upload the results")
def linkextractor(n_runs, only_result, uploadresult):
    """Micro-benchmark for LinkExtractor()"""
    arg = "python link.py"
    calculator("LinkExtractor", arg, n_runs, only_result, uploadresult)


@cli.command()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option('--uploadresult', is_flag=True, help="Upload the results")
def xpathbench(n_runs, only_result, uploadresult):
    """Micro-benchmark for extraction using xpath"""
    arg = "python xpathbench.py"
    calculator("Xpath Benchmark", arg, n_runs, only_result, uploadresult)
