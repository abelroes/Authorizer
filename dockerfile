# syntax=docker/dockerfile:1
FROM python:3.8.10
WORKDIR /authorizer
COPY . .
RUN pip install -r requirements.txt
RUN cd src/ && python -m pytest
ENTRYPOINT [ "python3", "src/main.py"]