# pull official base image
FROM python:3.10-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml ./
COPY ./poetry.lock ./
RUN poetry install

# add app
COPY . .
