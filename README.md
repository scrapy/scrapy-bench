# Benchmarking CLI for Scrapy
(The project is still in development.)

>A command-line interface for benchmarking Scrapy, that reflects real-world usage.

## Why?

* Currently, the `scrapy bench` option present just spawns a spider which aggresively crawls randomly generated links at a high speed. 
* The speed thus obtained, which maybe useful for comparisons, does not actually reflects a real-world scenario.
* The actual speed varies with the python version and scrapy version.

### Current Features 
* Spawns a CPU-intensive spider which follows a fixed number of links of a static snapshot of the site [Books to Scrape](http://books.toscrape.com/index.html).
* Follows a real-world scenario where various information of the books is extracted, and stored in a `.csv` file.
* Has a `--n-runs` option for perfoming more than one iteration of spider to improve the precision.
* Has a `--only_results` option for viewing the results only.
* A micro benchmark that tests LinkExtractor() function by extracting links from a collection of html pages.
* A micro benchmark that tests extraction using xpath from a collection of html pages.

## Installation

### For Ubuntu

* Firstly, download the static snapshot of the website [Books to Scrape](http://books.toscrape.com/index.html). That can be done by using `wget`.

    `wget --mirror --convert-links --adjust-extension --page-requisites --no-parent http://books.toscrape.com/index.html`

* Then place the whole file in the folder `var/www/html`.
* `nginx` is required for deploying the website. Hence it is required to be installed and configured. If it is, you would be able to see the site [here](http://localhost/books.toscrape.com/index.html). 
* If not, then follow the given steps :
        
        sudo apt-get update
        sudo apt-get install nginx
  
  Before we can test Nginx, we need to reconfigure our firewall software to allow access to the service. Nginx registers itself as a service with `ufw`, our firewall, upon installation.
  We can list the applications configurations that ufw knows how to work with by typing:

        sudo ufw app list

    You should get a listing of the application profiles:

        Available applications:
          Nginx Full
          Nginx HTTP
          Nginx HTTPS
          OpenSSH
   
   Do the following to allow Nginx through the firewall : 
          
          sudo ufw allow 'Nginx HTTP'
   
   You can verify the change by typing:

          sudo ufw status
   
   We can check with the systemd init system to make sure the service is running by typing:

          systemctl status nginx

  
My Nginx config file is shared [here](https://github.com/Parth-Vader/Scrapy-BenchCLI/blob/master/nginx.conf).
 Source : [How to install nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04).

The html files present in `sites.tar.gz` file were downloaded using a `scrapy spider` from the top sites from `Alexa top sites` list.

The html files present in `bookfiles.tar.gz` were downloaded using a `scrapy spider` from the website [Books to Scrape](http://books.toscrape.com/index.html).

* Do the following to complete the installation:
    
      git clone https://github.com/Parth-Vader/Scrapy-BenchCLI.git  
      cd scrapy-bench/  
      virtualenv env  
      . env/bin/activate   
      pip install --editable .
      tar -xvzf sites.tar.gz
      tar -xvzf bookfiles.tar.gz
    
## Usage
  
	Usage: scrapy-bench [OPTIONS] COMMAND [ARGS]...

	  A benchmark suite for Scrapy.

	Options:
	  --help  Show this message and exit.

	Commands:
	  bookworm       Spider to scrape locally hosted site
	  linkextractor  Micro-benchmark for LinkExtractor()
	  xpathbench     Micro-benchmark for extraction using xpath

