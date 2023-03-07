#!/bin/bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for postgres..."
  sleep 0.5
done
echo "PostgreSQL started"

exec "$@"