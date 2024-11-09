# !/bin/bash

docker rm -f agent-zero-exe

cp -rf python/aci docker/

cd docker

docker build -t my-image .

rm -rf aci
