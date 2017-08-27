FROM ubuntu:16.04

WORKDIR /scrapy-bench

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Download books.toscrape.com
RUN apt update && \
    apt install -y wget
RUN wget -q \
    --mirror --convert-links --adjust-extension --page-requisites --no-parent \
    http://books.toscrape.com/index.html

# Install pyenv with dependencies
RUN apt update && \
    apt install -y git nginx \
    make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev
RUN cd / && git clone https://github.com/pyenv/pyenv.git
ENV PYENV_ROOT /pyenv
ENV PATH $PYENV_ROOT/bin:$PATH

# Install python versions for benchmarking
RUN pyenv install 2.7.13
RUN pyenv install 3.5.4
RUN pyenv install 3.6.2
# pypy3.5-5.8.0
# pypy2.7-5.8.0
RUN ln -s /pyenv/versions/2.7.13/bin/python /usr/bin/python2.7 && \
    ln -s /pyenv/versions/3.5.4/bin/python /usr/bin/python3.5 && \
    ln -s /pyenv/versions/3.6.2/bin/python /usr/bin/python3.6

# Install tox
RUN python3.6 -m pip install tox --user
ENV PATH /root/.local/bin:$PATH

# Initialize all tox environments
COPY setup.py .
COPY tox.ini .
# make an emapty bench.py to just generate all environments
RUN touch bench.py && tox

# Set up bookworm benchmark
RUN ln -s `pwd`/books.toscrape.com /var/www/html/

# Set up broadworm benchmark
RUN python3.6 -m pip install six twisted

COPY . .

ENTRYPOINT ["bash", "tox-entrypoint.sh"]
