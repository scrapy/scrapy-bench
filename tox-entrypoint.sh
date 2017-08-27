#!/usr/bin/env bash
set -ev

# An entry point for the docker container:
# change /etc/hosts, start nginx and the broad server.

service nginx start
python3.6 \
    -c 'print("\n".join(f"127.0.0.1    domain{i}" for i in range(1, 1001)))' \
    >> /etc/hosts
python3.6 server.py &

tox $*
