FROM python:3.11-slim-buster

# Build dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y procps \

# copy code
COPY ./ app/
WORKDIR ./app

# Pip dependencies
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_trf
RUN python -m spacy download fr_core_news_sm

# Port
EXPOSE 80

CMD /bin/bash
