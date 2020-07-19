import subprocess
import os

import click
import statistics
import scrapy

import codespeedinfo


class commandoption(object):
    def __init__(self, n_runs, only_result, upload_result, book_url, vmprof, set):
        self.n_runs = n_runs
        self.only_result = only_result
        self.upload_result = upload_result
        self.book_url = book_url
        self.vmprof = vmprof
        self.set = set


def calculator(
        test,
        arg,
        n_runs,
        only_result,
        upload_result=False,
        vmprof=False,
        workpath=os.getcwd()):
    w = []
    command = 'python {}'.format(arg)
    if vmprof:
        command = 'python -m vmprof --web {}'.format(arg)

    for x in range(n_runs):
        if only_result:
            process = subprocess.Popen(
                command,
                cwd=workpath,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            process.wait()
        else:
            process = subprocess.Popen(command, cwd=workpath, shell=True)
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


@click.group(chain=True)
@click.option(
    '--n-runs',
    default=1,
    help="Take multiple readings for the benchmark.")
@click.option('--only_result', is_flag=True, help="Display the results only.")
@click.option(
    '--upload_result',
    is_flag=True,
    help="Upload the results to local codespeed")
@click.option(
    '--book_url',
    default="http://localhost/books.toscrape.com/",
    help="Use with bookworm command. The url to book.toscrape.com on your local machine")
@click.option('--vmprof',
    is_flag=True,
    help="Profiling benchmarkers with Vmprof and upload the result to the web")
@click.option(
    '--set',
    '-s',
    multiple=True,
    help="Settings to be passed to the Scrapy command. Use with the bookworm/broadworm commands.")


@click.pass_context
def cli(ctx, n_runs, only_result, upload_result, book_url, vmprof, set):
    """A benchmark suite for Scrapy."""
    ctx.obj = commandoption(n_runs, only_result, upload_result, book_url, vmprof, set)


@cli.command()
@click.pass_obj
def bookworm(obj):
    """Spider to scrape locally hosted site"""
    scrapy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'execute.py')
    workpath = os.path.join(os.getcwd(), "books")
    settings = " ".join("-s %s" % s for s in obj.set)
    arg = "%s crawl followall -o items.csv -a book_url=%s %s" % (scrapy_path, obj.book_url, settings)

    calculator(
        "Book Spider",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.pass_obj
def broadworm(obj):
    """Broad crawl spider to scrape locally hosted sites"""
    scrapy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'execute.py')
    workpath = os.path.join(os.getcwd(), "broad")
    settings = " ".join("-s %s" % s for s in obj.set)
    arg = "%s crawl broadspider -o items.csv %s" % (scrapy_path, settings)

    calculator(
        "Broad Crawl",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.pass_obj
def linkextractor(obj):
    """Micro-benchmark for LinkExtractor()"""
    arg = "link.py"

    calculator(
        "LinkExtractor",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof)


@cli.command()
@click.pass_obj
def cssbench(obj):
    """Micro-benchmark for extraction using css"""
    arg = "cssbench.py"

    calculator(
        "css Benchmark",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof)


@cli.command()
@click.pass_obj
def xpathbench(obj):
    """Micro-benchmark for extraction using xpath"""
    arg = "xpathbench.py"

    calculator(
        "xpath Benchmark",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof)


@cli.command()
@click.pass_obj
def itemloader(obj):
    """Item loader benchmarker"""
    arg = "itemloader.py"

    calculator(
        "Item Loader benchmarker",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof)


@cli.command()
@click.pass_obj
def urlparseprofile(obj):
    """Urlparse benchmarker"""
    arg = "urlparseprofile.py"

    calculator(
        "Urlparse benchmarker",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof)


if __name__ == '__main__':
    cli()
