#!/bin/bash

cd /home/sport-be || exit 1

git pull

docker-compose stop
docker image prune -a -f
docker-compose -f docker-compose.yml --env-file .env up --build --remove-orphans -d