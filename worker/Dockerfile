FROM python:3.7-alpine

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    rm -rf /var/cache/apk/*
COPY . /worker
WORKDIR /worker

RUN pip install -r requirements.txt

RUN apk del build-deps gcc musl-dev
RUN apk add ffmpeg
ENV REDIS_URL="redis://redis:6379"
ENV UPLOAD_URL="http://app:8000/uploadfromworker"

ENTRYPOINT [ "celery", "-A", "tasks", "worker", "--loglevel=info" ]