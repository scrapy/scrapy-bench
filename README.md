# Benchmarking CLI for Scrapy
(The project is still in development.)

>A command-line interface for benchmarking Scrapy, that reflects real-world usage.

## Why?

* Currently, the `scrapy bench` option present just spawns a spider which aggressively crawls randomly generated links at a high speed.
* The speed thus obtained, which maybe useful for comparisons, does not actually reflects a real-world scenario.
* The actual speed varies with the python version and scrapy version.

### Current Features
* Spawns a CPU-intensive spider which follows a fixed number of links of a static snapshot of the site [Books to Scrape](http://books.toscrape.com/index.html).
* Follows a real-world scenario where various information of the books is extracted, and stored in a `.csv` file.
* A broad crawl benchmark that uses 1000 copies of the site [Books to Scrape](http://books.toscrape.com/index.html) which are dynamically generated using `twisted`. The server file is present [here](https://github.com/scrapy/scrapy-bench/blob/master/server.py).
* A micro benchmark that tests LinkExtractor() function by extracting links from a collection of html pages.
* A micro benchmark that tests extraction using css from a collection of html pages.
* A micro benchmark that tests extraction using xpath from a collection of html pages
* Profile the benchmarkers with **vmprof** and upload to their website

### Options
* `--n-runs` option for performing more than one iteration of spider to improve the precision.
* `--only_result` option for viewing the results only.
* `--upload_result` option to upload the results to local codespeed for better comparison.

### Spider settings
* `SCRAPY_BENCH_RANDOM_PAYLOAD_SIZE`: Adds a random payload with the given size (in bytes).

## Setup

### Setup server for Ubuntu

* Firstly, download the static snapshot of the website [Books to Scrape](http://books.toscrape.com/index.html). That can be done by using `wget`.

        wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
            http://books.toscrape.com/index.html

* Then place the whole file in the folder `var/www/html`:

        sudo ln -s `pwd`/books.toscrape.com/ /var/www/html/

* `nginx` is required for deploying the website. Hence it is required to be installed and configured. If it is, you would be able to see the site [here](http://localhost/books.toscrape.com/index.html).
* If not, then follow the given steps :

        sudo apt-get update
        sudo apt-get install nginx

* For the broad crawl, use the `server.py` file to serve sites of local copy of [Books to Scrape](http://books.toscrape.com/index.html), which would already be in `/var/www/html`.

### Setup server using docker

* Build serve part using docker

        docker build -t scrapy-bench-server -f docker/Dockerfile .

* Run docker container

        docker run --rm -ti --network=host scrapy-bench-server

* Now you have [nginx](http://localhost:8000/index.html) and [serve.py](http://localhost:8880/index.html) serving

### Client setup

* Add the following entries to `/etc/hosts` file :

	  127.0.0.1    domain1
	  127.0.0.1    domain2
	  127.0.0.1    domain3
	  127.0.0.1    domain4
	  127.0.0.1    domain5
	  127.0.0.1    domain6
	  127.0.0.1    domain7
	  127.0.0.1    domain8
	  ....................
	  127.0.0.1    domain1000

* This would point the sites `http://domain1:8880/index.html` to the original site generated at `http://localhost:8880/index.html`.


There are 130 html files present in `sites.tar.gz`, which were downloaded using `download.py` from the top sites from `Alexa top sites` list.

There are 200 html files present in `bookfiles.tar.gz`, which were downloaded using `download.py` from the website [Books to Scrape](http://books.toscrape.com/index.html).

The spider `download.py`, dumps the response body as unicode to the files. The list of top sites was taken from [here](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip).

* Do the following to complete the installation:

      git clone https://github.com/scrapy/scrapy-bench.git
      cd scrapy-bench/
      virtualenv env
      . env/bin/activate
      pip install --editable .

## Usage

	Usage: scrapy-bench [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

	  A benchmark suite for Scrapy.

	Options:
	  --n-runs INTEGER  Take multiple readings for the benchmark.
	  --only_result     Display the results only.
	  --upload_result   Upload the results to local codespeed
	  --book_url TEXT   Use with bookworm command. The url to book.toscrape.com on
	                    your local machine

	  --vmprof          Profling benchmarkers with Vmprof and upload the result to
	                    the web

	  -s, --set TEXT    Settings to be passed to the Scrapy command. Use with the
	                    bookworm/broadworm commands.

	  --help            Show this message and exit.

	Commands:
	  bookworm         Spider to scrape locally hosted site
	  broadworm        Broad crawl spider to scrape locally hosted sites
	  cssbench         Micro-benchmark for extraction using css
	  csv              Visit URLs from a CSV file
	  itemloader       Item loader benchmarker
	  linkextractor    Micro-benchmark for LinkExtractor()
	  urlparseprofile  Urlparse benchmarker
	  xpathbench       Micro-benchmark for extraction using xpath
