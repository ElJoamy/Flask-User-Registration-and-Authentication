#!/bin/bash

docker network create -d macvlan \
  --subnet=192.168.232.0/24 \
  --gateway=192.168.232.2 \
  -o parent=ens33 \
  redInternet