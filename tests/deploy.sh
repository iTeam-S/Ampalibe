#!/bin/bash

# Build the framework
docker build . -t ampalibe

# run a container
docker run -d -v "${PWD}/tests/app:/usr/src/app" -p 4555:4555 --name amp ampalibe

# Attente de stabilité du serveur
sleep 2
