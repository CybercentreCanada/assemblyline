FROM python:3.9-slim-buster AS base

# Upgrade dist packages
RUN apt-get update && apt-get -yy upgrade && rm -rf /var/lib/apt/lists/*

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy libffi6 libfuzzy2 libmagic1 \
  && rm -rf /var/lib/apt/lists/*

# Patch Python 3.9 for FIPS - https://github.com/python/cpython/issues/95231 (Not necessary for Python 3.10+)
RUN sed -i -e 's/if e.errno == errno.EINVAL:/if e.errno in {errno.EINVAL, errno.EPERM, errno.ENOSYS}:/g' /usr/local/lib/python3.9/crypt.py
