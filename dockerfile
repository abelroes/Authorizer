# syntax=docker/dockerfile:1
FROM python:3.8.10 AS tester
WORKDIR /authorizer
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN cd src/ && python -m pytest


FROM python:3.8.10 AS builder
WORKDIR /authorizer
ENTRYPOINT [ "python3", "src/main.py"]