#!/bin/bash
mongo_ready() {
    $(which curl) http://${MONGO_HOST:-localhost}:${MONGO_PORT:-27017} | grep 'access'
}

until mongo_ready; do
  >&2 echo 'Waiting for MongoDB to become available...'
  sleep 1
done
>&2 echo 'MongoDB is available.'

gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker