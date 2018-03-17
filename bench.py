import subprocess
import os

import click
import statistics

import codespeedinfo


class commandoption(object):
    def __init__(self, n_runs, only_result, upload_result, book_url, vmprof):
        self.n_runs = n_runs
        self.only_result = only_result
        self.upload_result = upload_result
        self.book_url = book_url
        self.vmprof = vmprof


def calculator(
        test,
        arg,
        n_runs,
        only_result,
        upload_result=False,
        vmprof=False,
        benchmarker='',
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

    if vmprof:
        mapping = {
            'cssbench': 'cssbench.py',
            'linkextractor': 'link.py',
            'xpathbench': 'xpathbench.py',
            'itemloader': 'itemloader.py'
        }

        try:
            arg = 'python -m vmprof --web {}'.format(mapping[benchmarker])
            process = subprocess.Popen(arg, shell=True)
            process.wait()

        except KeyError:
            click.echo('The benchmarker you entered is invalid')

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
    help="Profling benchmarkers with Vmprof and upload the result to the web")
@click.pass_context
def cli(ctx, n_runs, only_result, upload_result, book_url, vmprof):
    """A benchmark suite for Scrapy."""
    ctx.obj = commandoption(n_runs, only_result, upload_result, book_url, vmprof)


@cli.command()
@click.pass_obj
def bookworm(obj):
    """Spider to scrape locally hosted site"""
    workpath = os.path.join(os.getcwd(), "books")
    arg = "scrapy crawl followall -o items.csv -a book_url=%s" % obj.book_url
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'bookworm'

    calculator(
        "Book Spider",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker,
        workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.pass_obj
def broadworm(obj):
    """Broad crawl spider to scrape locally hosted sites"""
    workpath = os.path.join(os.getcwd(), "broad")
    arg = "scrapy crawl broadspider -o items.csv"
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'broadworm'

    calculator(
        "Broad Crawl",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker,
        workpath)
    os.remove(os.path.join(workpath, "items.csv"))


@cli.command()
@click.pass_obj
def linkextractor(obj):
    """Micro-benchmark for LinkExtractor()"""
    arg = "python link.py"
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'linkextractor'

    calculator(
        "LinkExtractor",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker)


@cli.command()
@click.pass_obj
def cssbench(obj):
    """Micro-benchmark for extraction using css"""
    arg = "python cssbench.py"
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'cssbench'

    calculator(
        "css Benchmark",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker)


@cli.command()
@click.pass_obj
def xpathbench(obj):
    """Micro-benchmark for extraction using xpath"""
    arg = "python xpathbench.py"
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'xpathbench'

    calculator(
        "xpath Benchmark",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker)


@cli.command()
@click.pass_obj
def itemloader(obj):
    """Item loader benchmarker"""
    workpath = os.path.join(os.getcwd())
    arg = "python itemloader.py"
    benchmarker = ''
    if obj.vmprof:
        benchmarker = 'itemloader'

    calculator(
        "Item Loader benchmarker",
        arg,
        obj.n_runs,
        obj.only_result,
        obj.upload_result,
        obj.vmprof,
        benchmarker)

if __name__ == '__main__':
    cli()
