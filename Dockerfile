FROM python:3.11-slim-buster

# Build dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y procps

# copy code

COPY ./ app/

WORKDIR ./app

# Pip dependencies
RUN pip install -r requirements.txt

# Port
EXPOSE 8501

# Healthcheck: test a container
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD /bin/bash

# CMD streamlit run --server.port 8501 --theme.base light  streamlit/accueil.py
