import subprocess
import os

import click
import statistics

import codespeedinfo

run = 1
result = False
upload = False


def calculator(
        test,
        arg,
        n_runs,
        only_result,
        uploadresult=False,
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

    if uploadresult is True:
        codespeedinfo.uploadresult(test, w)

    os.remove(os.path.join(workpath, "Benchmark.txt"))


@click.group()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark.")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option('--uploadresult', is_flag=True, help="Upload the results")
def cli(n_runs, only_result, uploadresult):
    """A benchmark suite for Scrapy."""
    global run, result, upload
    run = n_runs
    result = only_result
    upload = uploadresult


@cli.command()
def bookworm():
    """Spider to scrape locally hosted site"""
    workpath = os.path.join(os.getcwd(), "books")
    arg = "scrapy crawl followall -o items.csv"
    calculator("Book Spider", arg, run, result, upload, workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
def linkextractor():
    """Micro-benchmark for LinkExtractor()"""
    arg = "python link.py"
    calculator("LinkExtractor", arg, run, result, upload)


@cli.command()
def xpathbench():
    """Micro-benchmark for extraction using xpath"""
    arg = "python xpathbench.py"
    calculator("Xpath Benchmark", arg, run, result, upload)
