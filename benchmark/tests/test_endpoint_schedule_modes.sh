#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
START_PS1="$ROOT_DIR/start_benchmark.ps1"
RUN_AB="$ROOT_DIR/benchmark/run_ab.sh"

require_line() {
  file="$1"
  pattern="$2"
  label="$3"
  if ! grep -Fq "$pattern" "$file"; then
    echo "[FAIL] missing $label: $pattern" >&2
    exit 1
  fi
}

require_line "$START_PS1" 'function Get-EndpointSchedule' 'endpoint schedule selector'
require_line "$START_PS1" 'function Get-EndpointPlan' 'endpoint plan resolver'
require_line "$START_PS1" 'Select Endpoint Execution Schedule:' 'schedule prompt'
require_line "$START_PS1" 'Peak Client Concurrency (XAMPP + NGINX-Multi)' 'peak concurrency summary'
require_line "$START_PS1" 'Load Hint:' 'load hint summary'
require_line "$START_PS1" '"-e", "ENDPOINT_SCHEDULE=$EndpointSchedule"' 'compose env passthrough'
require_line "$START_PS1" '"-e", "CPU_DURATION=$cpuDuration"' 'cpu duration passthrough'
require_line "$START_PS1" '"-e", "IO_CONNECTIONS=$ioConnections"' 'io connections passthrough'
require_line "$START_PS1" 'Enter duration in seconds (min: 10):' 'custom per-endpoint duration prompt'
require_line "$RUN_AB" 'ENDPOINT_SCHEDULE=${ENDPOINT_SCHEDULE:-sequential}' 'run_ab default schedule'
require_line "$RUN_AB" 'CPU_DURATION=${CPU_DURATION:-$DURATION}' 'cpu duration env default'
require_line "$RUN_AB" 'CPU_CONNECTIONS=${CPU_CONNECTIONS:-$CONNECTIONS}' 'cpu connections env default'
require_line "$RUN_AB" 'endpoint_duration_for()' 'endpoint duration helper'
require_line "$RUN_AB" 'endpoint_connections_for()' 'endpoint connections helper'
require_line "$RUN_AB" 'if [ "$ENDPOINT_SCHEDULE" = "parallel" ]; then' 'parallel branch'
require_line "$RUN_AB" 'merge_endpoint_results "$endpoint"' 'result merge flow'

echo "[PASS] test_endpoint_schedule_modes.sh"
