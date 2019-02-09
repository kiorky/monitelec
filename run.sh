#!/usr/bin/env bash
img=kiorky/monitelec
set -e

DC_FILES="docker-compose.yml"
if [ -f o.yml ];then
    DC_FILES="$DC_FILES -f o.yml"
fi
build() { docker-compose build; }
if ! (build >/dev/null 2>&1);then
    docker-compose build
fi
docker-compose run --rm monit
# vim:set et sts=4 ts=4 tw=80:
