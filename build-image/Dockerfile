# Same as the root image, but we keep the dev dependencies
ARG base
ARG tag
FROM $base:$tag

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy build-essential libffi-dev libfuzzy-dev \
  && rm -rf /var/lib/apt/lists/*
