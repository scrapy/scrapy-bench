FROM ubuntu:16.04

# Install pyenv with dependencies
RUN apt update && \
    apt install -y git make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev
RUN git clone https://github.com/pyenv/pyenv.git
ENV PYENV_ROOT /pyenv
ENV PATH $PYENV_ROOT/bin:$PATH

# Install python versions for benchmarking
RUN pyenv install 2.7.13
RUN pyenv install 3.5.4
RUN pyenv install 3.6.2
# pypy3.5-5.8.0
# pypy2.7-5.8.0
RUN ln -s /pyenv/versions/2.7.13/bin/python /usr/bin/python2.7
RUN ln -s /pyenv/versions/3.5.4/bin/python /usr/bin/python3.5
RUN ln -s /pyenv/versions/3.6.2/bin/python /usr/bin/python3.6

# Install tox
RUN python3.6 -m pip install tox --user
ENV PATH /root/.local/bin:$PATH

WORKDIR /scrapy-bench
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Initialize all tox environments
COPY setup.py .
COPY tox.ini .
# make an emapty bench.py to just generate all environments
RUN touch bench.py
RUN tox

COPY . .
