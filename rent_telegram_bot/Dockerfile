# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /rent_telegram_bot
COPY requirements.txt /rent_telegram_bot/
RUN pip install -r requirements.txt
COPY . /rent_telegram_bot/
