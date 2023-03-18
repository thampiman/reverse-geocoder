#!/bin/bash
set -e

docker build -t reverse-geocoder-whl .
docker run \
	--rm \
	-it \
	-v "$(pwd)"/dist:/app/dist \
	-v "$(pwd)"/wheelhouse:/app/wheelhouse \
	-v /var/run/docker.sock:/var/run/docker.sock \
	reverse-geocoder-whl \
	pipx run cibuildwheel --platform linux
