#!/usr/bin/env bash

docker build -t registry.gitlab.com/smncd/galette . &&
docker push registry.gitlab.com/smncd/galette