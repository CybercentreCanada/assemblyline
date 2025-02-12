FROM python:3.11-slim-bookworm AS base

# Upgrade dist packages
RUN apt-get update && apt-get -yy upgrade && rm -rf /var/lib/apt/lists/*

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy libffi8 libfuzzy2 libmagic1 git\
  && rm -rf /var/lib/apt/lists/*

# Update setuptools package
RUN pip install -U setuptools
