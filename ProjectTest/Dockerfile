FROM python:3.10-slim

ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE} -I
