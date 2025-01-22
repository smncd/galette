#!/usr/bin/env bash

docker build -f ./binary/Dockerfile -t galette-pyinstaller .

docker run --rm -v "$(pwd):/app" galette-pyinstaller \
    pyinstaller galette/__main__.py \
    --name 'galette' \
    --distpath './binary/dist' \
    --workpath './binary/build' \
    --specpath './binary/' \
    --onefile \
    --clean