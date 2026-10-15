FROM python:3.14-slim-trixie AS base

# Upgrade dist packages
RUN apt-get update && apt-get -yy upgrade && rm -rf /var/lib/apt/lists/*

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy libmagic1 git\
  && rm -rf /var/lib/apt/lists/*

# Update setuptools package
RUN pip install -U setuptools pip
