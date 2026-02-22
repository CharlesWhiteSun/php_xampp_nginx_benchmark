#!/bin/sh
set -eu

# Helper: generate config.json from template and perform placeholder replacements
# Uses environment variables: DURATION, TOTAL_DURATION, ENDPOINT_SCHEDULE, CONNECTIONS,
# CPU_DURATION, JSON_DURATION, IO_DURATION, CPU_CONNECTIONS, JSON_CONNECTIONS, IO_CONNECTIONS,
# ITER, JSON_N, IO_SIZE, IO_ITER, IO_MODE

RESULTS_DIR=${RESULTS_DIR:-../results}
RUN_ID=$(date +%Y%m%d_%H%M%S)
OUT_DIR="${RESULTS_DIR%/}/${RUN_ID}"
mkdir -p "$OUT_DIR"
CONFIG_FILE="${OUT_DIR}/config.json"

cat > "$CONFIG_FILE" <<'CONFIGEOF'
{
    "duration": TOTAL_DURATION_VAL,
    "per_endpoint_duration": PER_ENDPOINT_DURATION_VAL,
    "endpoint_schedule": "ENDPOINT_SCHEDULE_VAL",
  "connections": CONNECTIONS_VAL,
  "endpoints": [
    "cpu.php",
    "json.php",
    "io.php"
  ],
  "endpoint_params": {
    "cpu": {
            "iterations": ITER_VAL,
            "duration": CPU_DURATION_VAL,
            "connections": CPU_CONNECTIONS_VAL
    },
    "json": {
            "items": JSON_N_VAL,
            "duration": JSON_DURATION_VAL,
            "connections": JSON_CONNECTIONS_VAL
    },
    "io": {
      "size": IO_SIZE_VAL,
      "iterations": IO_ITER_VAL,
            "mode": "IO_MODE_VAL",
            "duration": IO_DURATION_VAL,
            "connections": IO_CONNECTIONS_VAL
    }
  },
  "test_time": "TEST_TIME_VAL"
}
CONFIGEOF

# Replace placeholders with actual values (use defaults if not set)
DURATION=${DURATION:-10}
TOTAL_DURATION=${TOTAL_DURATION:-$DURATION}
ENDPOINT_SCHEDULE=${ENDPOINT_SCHEDULE:-sequential}
CONNECTIONS=${CONNECTIONS:-50}
CPU_DURATION=${CPU_DURATION:-$DURATION}
JSON_DURATION=${JSON_DURATION:-$DURATION}
IO_DURATION=${IO_DURATION:-$DURATION}
CPU_CONNECTIONS=${CPU_CONNECTIONS:-$CONNECTIONS}
JSON_CONNECTIONS=${JSON_CONNECTIONS:-$CONNECTIONS}
IO_CONNECTIONS=${IO_CONNECTIONS:-$CONNECTIONS}
ITER=${ITER:-10000}
JSON_N=${JSON_N:-2000}
IO_SIZE=${IO_SIZE:-8192}
IO_ITER=${IO_ITER:-20}
IO_MODE=${IO_MODE:-memory}

sed -i "s/PER_ENDPOINT_DURATION_VAL/$DURATION/g" "$CONFIG_FILE"
sed -i "s/TOTAL_DURATION_VAL/$TOTAL_DURATION/g" "$CONFIG_FILE"
sed -i "s/ENDPOINT_SCHEDULE_VAL/$ENDPOINT_SCHEDULE/g" "$CONFIG_FILE"
sed -i "s/CONNECTIONS_VAL/$CONNECTIONS/g" "$CONFIG_FILE"
sed -i "s/CPU_DURATION_VAL/$CPU_DURATION/g" "$CONFIG_FILE"
sed -i "s/JSON_DURATION_VAL/$JSON_DURATION/g" "$CONFIG_FILE"
sed -i "s/IO_DURATION_VAL/$IO_DURATION/g" "$CONFIG_FILE"
sed -i "s/CPU_CONNECTIONS_VAL/$CPU_CONNECTIONS/g" "$CONFIG_FILE"
sed -i "s/JSON_CONNECTIONS_VAL/$JSON_CONNECTIONS/g" "$CONFIG_FILE"
sed -i "s/IO_CONNECTIONS_VAL/$IO_CONNECTIONS/g" "$CONFIG_FILE"
sed -i "s/IO_ITER_VAL/$IO_ITER/g" "$CONFIG_FILE"
sed -i "s/ITER_VAL/$ITER/g" "$CONFIG_FILE"
sed -i "s/JSON_N_VAL/$JSON_N/g" "$CONFIG_FILE"
sed -i "s/IO_SIZE_VAL/$IO_SIZE/g" "$CONFIG_FILE"
sed -i "s/IO_MODE_VAL/$IO_MODE/g" "$CONFIG_FILE"
sed -i "s/TEST_TIME_VAL/$(date -u +%Y-%m-%dT%H:%M:%SZ)/g" "$CONFIG_FILE"

# Cleanup accidental placeholder prefixes if present
sed -i -r 's/CPU_([0-9]+)/\1/g' "$CONFIG_FILE" || true
sed -i -r 's/JSON_([0-9]+)/\1/g' "$CONFIG_FILE" || true
sed -i -r 's/IO_([0-9]+)/\1/g' "$CONFIG_FILE" || true

echo "$CONFIG_FILE"
