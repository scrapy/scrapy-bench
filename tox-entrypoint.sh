#!/usr/bin/env bash
set -ev

bash start-servers.sh

tox $*
