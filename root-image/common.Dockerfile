FROM python:3.9-slim-buster AS base

# Upgrade dist packages
RUN apt-get update && apt-get -yy upgrade && rm -rf /var/lib/apt/lists/*

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy libffi6 libfuzzy2 libmagic1 \
  && rm -rf /var/lib/apt/lists/*
