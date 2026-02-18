#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
RUN_AB="$ROOT_DIR/benchmark/run_ab.sh"

usage_count=$(grep -Ec 'ab -l -t "\$DURATION" -n "\$MAX_REQUESTS" -c "\$CONNECTIONS" -q "\$url"' "$RUN_AB")
if [ "$usage_count" -lt 3 ]; then
  echo "[FAIL] run_ab.sh must use ApacheBench -l flag in all benchmark invocations (found $usage_count)" >&2
  exit 1
fi

echo "[PASS] test_ab_command_flags.sh"
