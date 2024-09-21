#!/usr/bin/env bash

set -x

python3 section3_automated_instrumentation/postgres/postgres_automated_instrumentation.py

google-chrome-stable http://localhost:16686/