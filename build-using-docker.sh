#!/bin/sh

set -ex

docker build --network=host \
    --build-arg http_proxy="$http_proxy" \
    --build-arg https_proxy="$https_proxy" \
    --build-arg no_proxy="$no_proxy" \
    -f Dockerfile.oraclelinux -t ucarp-rpm-builder:oraclelinux-7 .

docker run --rm -it \
    -e http_proxy="$http_proxy" \
    -e https_proxy="$https_proxy" \
    -e no_proxy="$no_proxy" \
    -v `pwd`:/rpm-build -w /rpm-build \
    --net=host \
    ucarp-rpm-builder:oraclelinux-7 \
    ./build.sh
