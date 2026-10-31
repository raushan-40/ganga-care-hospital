#!/usr/bin/env bash
# Measures Time To Recovery: kills the container, polls /health until it returns 200.
# Usage: ./scripts/ttr_test.sh [URL] [RUNS]   (run on the host where Docker runs)
URL=${1:-http://localhost/health}; RUNS=${2:-3}; C=hospital-web; total=0
for i in $(seq 1 "$RUNS"); do
  until curl -fs -o /dev/null "$URL"; do sleep 1; done
  start=$(date +%s.%N); docker kill "$C" >/dev/null
  echo "Run $i: crashed at $(date +%T)"
  until curl -fs -o /dev/null --max-time 1 "$URL"; do sleep 0.2; done
  ttr=$(echo "$(date +%s.%N) - $start" | bc); total=$(echo "$total + $ttr" | bc)
  echo "Run $i: recovered, TTR = ${ttr}s"; sleep 5
done
echo "Average TTR over $RUNS runs: $(echo "scale=2; $total / $RUNS" | bc)s"
