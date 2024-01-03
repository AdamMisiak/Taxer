FROM python:3.11-slim

WORKDIR /app

COPY ./app/entrypoint.sh /app/entrypoint.sh
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings