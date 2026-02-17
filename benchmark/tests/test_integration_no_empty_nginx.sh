#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$ROOT_DIR"

docker-compose run --rm -e DURATION=20 -e TOTAL_DURATION=60 -e CONNECTIONS=200 benchmark >/tmp/benchmark_integration.log 2>&1 || {
  cat /tmp/benchmark_integration.log >&2
  echo "[FAIL] benchmark container run failed" >&2
  exit 1
}

latest_dir=$(ls -1dt results/*/ | head -n 1)
[ -n "$latest_dir" ] || {
  echo "[FAIL] no results directory found" >&2
  exit 1
}

csv_file="${latest_dir%/}/results.csv"
[ -f "$csv_file" ] || {
  echo "[FAIL] results.csv not found: $csv_file" >&2
  exit 1
}

for ep in cpu.php json.php io.php; do
  if ! grep -q "nginx_multi,$ep" "$csv_file"; then
    echo "[FAIL] missing nginx_multi row for endpoint $ep" >&2
    exit 1
  fi
done

if grep "nginx_multi" "$csv_file" | grep -q ",0ms,0,0,0,0,"; then
  echo "[FAIL] found nginx rows with full-zero latency percentile block" >&2
  grep "nginx_multi" "$csv_file" >&2
  exit 1
fi

echo "[PASS] test_integration_no_empty_nginx.sh"
