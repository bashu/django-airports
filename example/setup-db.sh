#!/usr/bin/env bash

# Fail if any command fails.
set -e

docker-compose exec web ./manage.py migrate --noinput
docker-compose exec web ./manage.py loaddata fixtures/initial_data
docker-compose exec web ./manage.py airports
