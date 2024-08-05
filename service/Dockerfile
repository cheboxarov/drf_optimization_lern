FROM python:3.9-alpine3.16

WORKDIR /service

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    apk add --no-cache postgresql-libs

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

COPY . /service

RUN adduser --disabled-password service-user

USER service-user

EXPOSE 8000