#!/usr/bin/env bash

docker compose -f deployment/demo.yml down
docker compose -f deployment/demo.yml pull
docker compose -f deployment/demo.yml up -d
