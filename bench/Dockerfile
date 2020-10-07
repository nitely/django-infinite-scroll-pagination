FROM python:3.7.2-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add  \
        postgresql-client \
        postgresql-dev \
        gcc \
        musl-dev \
        make \
        libffi-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip \
    && pip install Django==2.2.8 \
    && pip install psycopg2-binary==2.8.6

CMD until pg_isready --username=postgres --host=database; do sleep 1; done;
ENTRYPOINT /bin/sh
