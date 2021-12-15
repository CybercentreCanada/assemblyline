FROM python:3.10-slim-bullseye AS base

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy libffi6 libfuzzy2 libmagic1 \
  && rm -rf /var/lib/apt/lists/*
