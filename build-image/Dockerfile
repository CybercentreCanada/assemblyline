# Same as the root image, but we keep the dev dependencies
ARG base
FROM $base

# Get required apt packages
RUN apt-get update \
  && apt-get install -yy build-essential libffi-dev libfuzzy-dev \
  && rm -rf /var/lib/apt/lists/*

# Install assemblyline dependencies, but don't keep assemblyline
RUN pip install --user assemblyline && pip uninstall assemblyline -y
RUN chmod 750 /root/.local/lib/python3.9/site-packages
