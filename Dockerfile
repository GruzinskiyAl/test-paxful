FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/transferer

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev\
    && rm -rf /var/cache/apk/*

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/transferer/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
