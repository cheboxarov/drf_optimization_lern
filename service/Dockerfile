FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt

COPY . /service

WORKDIR /service

EXPOSE 8000

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    apk add --no-cache postgresql-libs


RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user