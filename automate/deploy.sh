#!/bin/bash

# Build the framework
docker build . -t ampalibe

# run a container
docker run -d -v "${PWD}/example/default:/usr/src/app" -p 4555:4555 --name amp ampalibe

sleep 2 

docker logs amp
