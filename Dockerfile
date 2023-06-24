FROM python:3.11-slim-buster

# Build dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y procps

# copy code
# COPY ./streamlit/Accueil.py app/Accueil.py
# COPY ./streamlit/pages/ app/Médecin Malgrè Lui.py
# COPY ./streamlit/content app/content

COPY ./streamlit app/

RUN rm app/pages/compare.py

WORKDIR ./app

# Pip dependencies
RUN pip install -r requirements.txt

# Port
EXPOSE 8501

# Healthcheck: test a container
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# CMD /bin/bash

CMD streamlit run --server.port 8501 --theme.base light  streamlit/Accueil.py
