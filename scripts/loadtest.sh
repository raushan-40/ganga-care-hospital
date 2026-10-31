#!/usr/bin/env bash
# Needs Apache Bench (apt install apache2-utils). Compare results to your SLA.
URL=${1:-http://localhost/}
ab -n 1000 -c 20 "$URL" | egrep "Requests per second|Time per request|Failed requests|50%|95%|99%"
