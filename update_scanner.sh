#!/bin/bash

cd scanner

docker compose pull
docker compose up -d --remove-orphans
docker image prune