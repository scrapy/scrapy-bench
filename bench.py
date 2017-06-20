import subprocess
import os

import click
import statistics

import codespeedinfo


class commandoption(object):
    def __init__(self, n_runs, only_result, upload_result):
        self.n_runs = n_runs
        self.only_result = only_result
        self.upload_result = upload_result


def calculator(
        test,
        arg,
        n_runs,
        only_result,
        upload_result=False,
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

    if upload_result:
        codespeedinfo.uploadresult(test, w)

    os.remove(os.path.join(workpath, "Benchmark.txt"))


@click.group()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark.")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option(
    '--upload_result',
    is_flag=True,
    help="Upload the results to local codespeed")
@click.pass_context
def cli(ctx, n_runs, only_result, upload_result):
    """A benchmark suite for Scrapy."""
    ctx.obj = commandoption(n_runs, only_result, upload_result)


@cli.command()
@click.pass_obj
def bookworm(obj):
    """Spider to scrape locally hosted site"""
    workpath = os.path.join(os.getcwd(), "books")
    arg = "scrapy crawl followall -o items.csv"
    calculator(
        "Book Spider",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.pass_obj
def linkextractor(obj):
    """Micro-benchmark for LinkExtractor()"""
    arg = "python link.py"
    calculator(
        "LinkExtractor",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result)


@cli.command()
@click.pass_obj
def xpathbench(obj):
    """Micro-benchmark for extraction using xpath"""
    arg = "python xpathbench.py"
    calculator(
        "Xpath Benchmark",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result)
