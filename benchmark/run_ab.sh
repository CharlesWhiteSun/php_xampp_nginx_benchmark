#!/bin/sh
set -eu

. /usr/local/bin/lib_ab_parse.sh

DURATION=${DURATION:-10}
PER_ENDPOINT_DURATION=${PER_ENDPOINT_DURATION:-$DURATION}
TOTAL_DURATION=${TOTAL_DURATION:-$DURATION}
CONNECTIONS=${CONNECTIONS:-50}
MAX_REQUESTS=${MAX_REQUESTS:-1000000000}
ITER=${ITER:-10000}
JSON_N=${JSON_N:-2000}
IO_SIZE=${IO_SIZE:-8192}
IO_ITER=${IO_ITER:-20}
IO_MODE=${IO_MODE:-memory}
ENDPOINTS=${ENDPOINTS:-"cpu.php json.php io.php"}
ENDPOINT_SCHEDULE=${ENDPOINT_SCHEDULE:-sequential}
CPU_DURATION=${CPU_DURATION:-$DURATION}
JSON_DURATION=${JSON_DURATION:-$DURATION}
IO_DURATION=${IO_DURATION:-$DURATION}
CPU_CONNECTIONS=${CPU_CONNECTIONS:-$CONNECTIONS}
JSON_CONNECTIONS=${JSON_CONNECTIONS:-$CONNECTIONS}
IO_CONNECTIONS=${IO_CONNECTIONS:-$CONNECTIONS}

# Normalize any accidental CPU_/JSON_/IO_ prefixes in connection envs
CPU_CONNECTIONS=${CPU_CONNECTIONS#CPU_}
JSON_CONNECTIONS=${JSON_CONNECTIONS#JSON_}
IO_CONNECTIONS=${IO_CONNECTIONS#IO_}

URL_XAMPP=${URL_XAMPP:-http://localhost:8081/}
URL_NGINX=${URL_NGINX:-http://localhost:8082/}
URL_NGINX_MULTI=${URL_NGINX_MULTI:-http://localhost:8083/}

RESULTS_DIR=${RESULTS_DIR:-../results}
RUN_ID=$(date +%Y%m%d_%H%M%S)
OUT_DIR="${RESULTS_DIR%/}/${RUN_ID}"
CSV_FILE="${OUT_DIR}/results.csv"
JSON_FILE="${OUT_DIR}/results.json"

mkdir -p "$OUT_DIR"
echo "timestamp,server,endpoint,requests_sec,latency_avg,latency_p50,latency_p75,latency_p90,latency_p99,transfer_sec" > "$CSV_FILE"
echo "[" > "$JSON_FILE"
JSON_FIRST=1

# Save benchmark configuration
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

# Replace placeholders with actual values
sed -i "s/PER_ENDPOINT_DURATION_VAL/$PER_ENDPOINT_DURATION/g" "$CONFIG_FILE"
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

# Cleanup any accidental placeholder prefixes left like CPU_50, JSON_50, IO_50
# (some environments or prior replacements could introduce tokens like CPU_50)
sed -i 's/CPU_\([0-9][0-9]*\)/\1/g' "$CONFIG_FILE" || true
sed -i 's/JSON_\([0-9][0-9]*\)/\1/g' "$CONFIG_FILE" || true
sed -i 's/IO_\([0-9][0-9]*\)/\1/g' "$CONFIG_FILE" || true

# Dump environment for diagnostics
env > "${OUT_DIR}/env_vars.txt"
wait_for() {
    name="$1"
    url="$2"
    echo "Waiting for ${name} at ${url}..."
    
    # ??敺?蝏?憪?
    sleep 2
    
    # 撠?雿輻 wget嚗蜓閬瘜?
    for i in $(seq 1 60); do
        if wget -q -O /dev/null "$url" 2>/dev/null; then
            echo "${name} is ready"
            return 0
        fi
        
        echo "  Attempt $i/60: ${name} not ready yet..."
        sleep 1
    done
    
    echo "WARNING: ${name} not responding after 60s, continuing anyway"
    return 0  # 銝葉甇ｇ?蝏抒賒?扯?
}

endpoint_url() {
    endpoint="$1"
    case "$endpoint" in
        cpu.php)
            echo "${endpoint}?n=${ITER}"
            ;;
        json.php)
            echo "${endpoint}?n=${JSON_N}"
            ;;
        io.php)
            echo "${endpoint}?size=${IO_SIZE}&iter=${IO_ITER}&mode=${IO_MODE}"
            ;;
        *)
            echo "$endpoint"
            ;;
    esac
}

endpoint_duration_for() {
    endpoint="$1"
    case "$endpoint" in
        cpu.php)
            echo "$CPU_DURATION"
            ;;
        json.php)
            echo "$JSON_DURATION"
            ;;
        io.php)
            echo "$IO_DURATION"
            ;;
        *)
            echo "$DURATION"
            ;;
    esac
}

endpoint_connections_for() {
    endpoint="$1"
    case "$endpoint" in
        cpu.php)
            echo "$CPU_CONNECTIONS"
            ;;
        json.php)
            echo "$JSON_CONNECTIONS"
            ;;
        io.php)
            echo "$IO_CONNECTIONS"
            ;;
        *)
            echo "$CONNECTIONS"
            ;;
    esac
}

run_ab() {
    name="$1"
    server="$2"
    endpoint="$3"
    url="$4"
    echo ""
    echo "=== ${name} :: ${endpoint} ==="
    
    # Run ab test with full output
    output=$(ab -l -t "$DURATION" -n "$MAX_REQUESTS" -c "$CONNECTIONS" -q "$url" 2>&1)
    echo "$output"

    parse_ab_output "$output" "$DURATION" "$CONNECTIONS"
    requests_sec="$PARSED_REQUESTS_SEC"
    latency_avg="$PARSED_LATENCY_AVG"
    p50="$PARSED_P50"
    p75="$PARSED_P75"
    p90="$PARSED_P90"
    p99="$PARSED_P99"
    transfer_sec="$PARSED_TRANSFER_SEC"
    
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${p50},${p75},${p90},${p99},${transfer_sec}" >> "$CSV_FILE"

    if [ "$JSON_FIRST" -eq 1 ]; then
        JSON_FIRST=0
    else
        echo "," >> "$JSON_FILE"
    fi

    printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
        "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$p50" "$p75" "$p90" "$p99" "$transfer_sec" >> "$JSON_FILE"

    echo "$output" > "${OUT_DIR}/${server}_${endpoint}.txt"
}

first_endpoint=$(echo "$ENDPOINTS" | awk '{print $1}')
first_path=$(endpoint_url "$first_endpoint")

wait_for "xampp" "${URL_XAMPP%/}/$first_path"
wait_for "nginx-multi" "${URL_NGINX_MULTI%/}/$first_path"

# Create temp directory for parallel results
TEMP_DIR="${OUT_DIR}/temp"
mkdir -p "$TEMP_DIR"

append_json_object() {
    obj_file="$1"
    if [ ! -f "$obj_file" ]; then
        return
    fi

    if [ "$JSON_FIRST" -eq 1 ]; then
        JSON_FIRST=0
    else
        echo "," >> "$JSON_FILE"
    fi
    cat "$obj_file" >> "$JSON_FILE"
}

merge_endpoint_results() {
    endpoint="$1"
    temp_csv_xampp="${TEMP_DIR}/${endpoint}_xampp.csv"
    temp_csv_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.csv"
    temp_json_xampp="${TEMP_DIR}/${endpoint}_xampp.json"
    temp_json_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.json"

    [ -f "$temp_csv_xampp" ] && cat "$temp_csv_xampp" >> "$CSV_FILE"
    [ -f "$temp_csv_nginx" ] && cat "$temp_csv_nginx" >> "$CSV_FILE"

    append_json_object "$temp_json_xampp"
    append_json_object "$temp_json_nginx"

    rm -f "$temp_csv_xampp" "$temp_csv_nginx" "$temp_json_xampp" "$temp_json_nginx"
}

run_endpoint_pair() {
    endpoint="$1"
    endpoint_duration="$2"
    endpoint_connections="$3"
    path=$(endpoint_url "$endpoint")
    temp_csv_xampp="${TEMP_DIR}/${endpoint}_xampp.csv"
    temp_csv_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.csv"
    temp_json_xampp="${TEMP_DIR}/${endpoint}_xampp.json"
    temp_json_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.json"

    echo "Endpoint: $endpoint"
    echo "  [$(date +'%H:%M:%S')] Starting XAMPP and NGINX-Multi in parallel..."

    (
        name="XAMPP (apache)"
        server="xampp"
        url="${URL_XAMPP%/}/$path"

        echo "" >&2
        echo "=== ${name} :: ${endpoint} ===" >&2

        ab_exit=0
        output=$(ab -l -t "$endpoint_duration" -n "$MAX_REQUESTS" -c "$endpoint_connections" -q "$url" 2>&1) || ab_exit=$?
        echo "$output" >&2
        if [ "$ab_exit" -ne 0 ]; then
            echo "[WARN] ab exited with code $ab_exit on ${server}/${endpoint}; continuing with parsed partial output." >&2
        fi

        parse_ab_output "$output" "$endpoint_duration" "$endpoint_connections"
        requests_sec="$PARSED_REQUESTS_SEC"
        latency_avg="$PARSED_LATENCY_AVG"
        p50="$PARSED_P50"
        p75="$PARSED_P75"
        p90="$PARSED_P90"
        p99="$PARSED_P99"
        transfer_sec="$PARSED_TRANSFER_SEC"

        timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${p50},${p75},${p90},${p99},${transfer_sec}" > "$temp_csv_xampp"
        printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
            "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$p50" "$p75" "$p90" "$p99" "$transfer_sec" > "$temp_json_xampp"
    ) &
    XAMPP_PID=$!

    (
        name="NGINX (multi-core, dynamic)"
        server="nginx_multi"
        url="${URL_NGINX_MULTI%/}/$path"

        echo "" >&2
        echo "=== ${name} :: ${endpoint} ===" >&2

        ab_exit=0
        output=$(ab -l -t "$endpoint_duration" -n "$MAX_REQUESTS" -c "$endpoint_connections" -q "$url" 2>&1) || ab_exit=$?
        echo "$output" >&2
        if [ "$ab_exit" -ne 0 ]; then
            echo "[WARN] ab exited with code $ab_exit on ${server}/${endpoint}; continuing with parsed partial output." >&2
        fi

        parse_ab_output "$output" "$endpoint_duration" "$endpoint_connections"
        requests_sec="$PARSED_REQUESTS_SEC"
        latency_avg="$PARSED_LATENCY_AVG"
        p50="$PARSED_P50"
        p75="$PARSED_P75"
        p90="$PARSED_P90"
        p99="$PARSED_P99"
        transfer_sec="$PARSED_TRANSFER_SEC"

        timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${p50},${p75},${p90},${p99},${transfer_sec}" > "$temp_csv_nginx"
        printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
            "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$p50" "$p75" "$p90" "$p99" "$transfer_sec" > "$temp_json_nginx"
    ) &
    NGINX_PID=$!

    wait $XAMPP_PID || echo "[WARN] XAMPP process returned non-zero for $endpoint" >&2
    wait $NGINX_PID || echo "[WARN] NGINX process returned non-zero for $endpoint" >&2

    echo "  [$(date +'%H:%M:%S')] ??Both tests completed for $endpoint"
    echo ""
}

echo ""
echo "=========================================="
echo "Running benchmark"
echo "=========================================="
if [ "$ENDPOINT_SCHEDULE" = "parallel" ]; then
    echo "Endpoint schedule: parallel (all endpoints run concurrently)"
    echo "Each endpoint test pair runs in parallel"
    total_expected=0
    for endpoint in $ENDPOINTS; do
        endpoint_duration=$(endpoint_duration_for "$endpoint")
        if [ "$endpoint_duration" -gt "$total_expected" ]; then
            total_expected="$endpoint_duration"
        fi
    done
    echo "Total expected time: ~${total_expected} seconds"
else
    echo "Endpoint schedule: sequential (endpoints run one by one)"
    echo "Each endpoint test pair runs in parallel"
    total_expected=0
    for endpoint in $ENDPOINTS; do
        endpoint_duration=$(endpoint_duration_for "$endpoint")
        total_expected=$((total_expected + endpoint_duration))
    done
    echo "Total expected time: ~${total_expected} seconds"
fi

echo "Endpoint stage allocation:"
for endpoint in $ENDPOINTS; do
    endpoint_duration=$(endpoint_duration_for "$endpoint")
    endpoint_connections=$(endpoint_connections_for "$endpoint")
    echo "  - ${endpoint}: duration=${endpoint_duration}s, connections=${endpoint_connections}"
done
echo "=========================================="
echo ""

if [ "$ENDPOINT_SCHEDULE" = "parallel" ]; then
    pid_refs=""
    for endpoint in $ENDPOINTS; do
        endpoint_duration=$(endpoint_duration_for "$endpoint")
        endpoint_connections=$(endpoint_connections_for "$endpoint")
        run_endpoint_pair "$endpoint" "$endpoint_duration" "$endpoint_connections" &
        pair_pid=$!
        pid_refs="$pid_refs ${pair_pid}:$endpoint"
    done

    for ref in $pid_refs; do
        pair_pid=${ref%%:*}
        endpoint=${ref#*:}
        wait "$pair_pid" || echo "[WARN] Endpoint pair process returned non-zero for $endpoint" >&2
    done

    for endpoint in $ENDPOINTS; do
        merge_endpoint_results "$endpoint"
    done
else
    for endpoint in $ENDPOINTS; do
        endpoint_duration=$(endpoint_duration_for "$endpoint")
        endpoint_connections=$(endpoint_connections_for "$endpoint")
        run_endpoint_pair "$endpoint" "$endpoint_duration" "$endpoint_connections"
        merge_endpoint_results "$endpoint"
    done
fi

# Remove trailing comma from JSON
sed -i '$ s/,$//' "$JSON_FILE"
# Clean up temp directory
rm -rf "$TEMP_DIR"

echo "" >> "$JSON_FILE"
echo "]" >> "$JSON_FILE"
echo "Results saved to ${OUT_DIR}"

