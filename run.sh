#!/usr/bin/env bash

docker build --tag test-task:latest -f ./src/Dockerfile ./src
export ID=$(docker run -dit test-task:latest /bin/bash)
docker exec $ID /bin/bash -c 'systemctl enable test-server && systemctl start test-server'
docker exec $ID /bin/bash -c '../test-framework/venv/bin/python3 -m pytest --host=127.0.0.1 --port=8899 api_test.py'
docker exec -it $ID /bin/bash
docker stop $ID && docker rm $ID && docker rmi test-task:latest
