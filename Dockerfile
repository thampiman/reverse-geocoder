FROM python:3.8-buster

RUN apt-get update
RUN apt-get install docker.io -y

RUN python -m pip install -U pip
RUN python -m pip install pipx

RUN mkdir /app
WORKDIR /app

COPY c++ .
COPY reverse_geocoder_whl .
COPY MANIFEST pyproject.toml README.md README.txt requirements.txt setup.py test.py .
