#!/bin/bash

docker network create my_test_network

docker build . -t api:1.0.0

cd teste/authentification
docker build . -t authentification:1.0.0

cd ../content
docker build . -t content:1.0.0

cd ../../
docker-compose up


