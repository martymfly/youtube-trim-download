FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

RUN apk del build-deps gcc musl-dev

COPY . /app
WORKDIR /app

ENV REDIS_URL="redis://redis:6379"

EXPOSE 8000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "--log-level", "INFO", "app:app" ]