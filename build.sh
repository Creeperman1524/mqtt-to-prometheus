#!/bin/bash

docker image rm mqtt-prometheus
docker build -t mqtt-prometheus .
