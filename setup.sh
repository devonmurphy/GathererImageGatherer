#!/usr/bin/env bash

clear
git --version >/dev/null 2>&1 || { echo >&2 "I require git but it's not installed. Aborting."; exit 1; }
docker --version >/dev/null 2>&1 || { echo >&2 "I require docker but it's not installed. Aborting."; exit 1; }
make --version >/dev/null 2>&1 || { echo >&2 "I require make but it's not installed. Aborting."; exit 1; }
python --version >/dev/null 2>&1 || { echo >&2 "I require python but it's not installed. Aborting."; exit 1; }
pip --version >/dev/null 2>&1 || { echo >&2 "I require pip but it's not installed. Aborting."; exit 1; }

docker pull jupyter/datascience-notebook:9b06df75e445
docker pull postgres
