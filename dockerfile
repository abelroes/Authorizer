# syntax=docker/dockerfile:1
FROM python:3.8.10
WORKDIR /authorizer
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# CMD [ "python3", "src/main.py"]
ENTRYPOINT [ "python3", "src/main.py"]