#!/usr/bin/env bash

set -x

curl localhost:8000/
curl localhost:8000/items/
curl localhost:8000/items/test

google-chrome-stable http://localhost:16686/ &