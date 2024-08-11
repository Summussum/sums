

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . .
WORKDIR /sums_sums
