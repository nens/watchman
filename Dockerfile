FROM ubuntu:xenial

MAINTAINER Carsten Byrman <carsten.byrman@nelen-schuurmans.nl>

# Get rid of debconf messages like "unable to initialize frontend: Dialog".
# https://github.com/docker/docker/issues/4032#issuecomment-192327844
ARG DEBIAN_FRONTEND=noninteractive

# `python bootstrap.py` succeeds on ubuntu:trusty, but fails on ubuntu:xenial
# with an SSL certificate error. Installing apt-transport-https helps.

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    build-essential \
    python-dev \
&& rm -rf /var/lib/apt/lists/*

# The -l option is to fix a problem with large user IDs (e.g. 1235227245).
# https://forums.docker.com/t/run-adduser-seems-to-hang-with-large-uid/27371/3
# https://github.com/moby/moby/issues/5419
ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid nens && useradd -lm -u $uid -g $gid nens

# Create and set the working directory for many instructions.
WORKDIR /code
USER nens
