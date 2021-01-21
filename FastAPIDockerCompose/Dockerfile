FROM python:3.8

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE} -I
