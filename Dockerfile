# Dockerfile

FROM python:3.12-alpine3.20

RUN mkdir /app
WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .