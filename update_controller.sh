#!/bin/bash

cd controller

docker compose pull
docker compose up -d --remove-orphans --build
docker image prune