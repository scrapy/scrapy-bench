import subprocess
import os
import sys
import time

import click
import statistics


def calculator(test, arg, n_runs, only_result, workpath=os.getcwd()):
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
def bookworm(n_runs, only_result):
    """Spider to scrape locally hosted site"""
    workpath = os.path.join(os.getcwd(), "books")
    arg = "scrapy crawl followall -o items.csv"
    calculator("Book Spider", arg, n_runs, only_result, workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark")
@click.option('--only_result', is_flag=True, help="Display the results only.")
def linkextractor(n_runs, only_result):
    """Micro-benchmark for LinkExtractor()"""
    arg = "python link.py"
    calculator("LinkExtractor", arg, n_runs, only_result)


@cli.command()
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark")
@click.option('--only_result', is_flag=True, help="Display the results only.")
def xpathbench(n_runs, only_result):
    """Micro-benchmark for extraction using xpath"""
    arg = "python xpathbench.py"
    calculator("Xpath Benchmark", arg, n_runs, only_result)
