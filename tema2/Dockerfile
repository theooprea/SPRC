FROM python:3.8.13-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /django-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

