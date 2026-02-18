#!/bin/sh
set -eu

. /usr/local/bin/lib_ab_parse.sh

DURATION=${DURATION:-10}
TOTAL_DURATION=${TOTAL_DURATION:-$DURATION}
CONNECTIONS=${CONNECTIONS:-50}
MAX_REQUESTS=${MAX_REQUESTS:-1000000000}
ITER=${ITER:-10000}
JSON_N=${JSON_N:-2000}
IO_SIZE=${IO_SIZE:-8192}
IO_ITER=${IO_ITER:-20}
IO_MODE=${IO_MODE:-memory}
ENDPOINTS=${ENDPOINTS:-"cpu.php json.php io.php"}

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
  "connections": CONNECTIONS_VAL,
  "endpoints": [
    "cpu.php",
    "json.php",
    "io.php"
  ],
  "endpoint_params": {
    "cpu": {
      "iterations": ITER_VAL
    },
    "json": {
      "items": JSON_N_VAL
    },
    "io": {
      "size": IO_SIZE_VAL,
      "iterations": IO_ITER_VAL,
      "mode": "IO_MODE_VAL"
    }
  },
  "test_time": "TEST_TIME_VAL"
}
CONFIGEOF

# Replace placeholders with actual values
sed -i "s/PER_ENDPOINT_DURATION_VAL/$DURATION/g" "$CONFIG_FILE"
sed -i "s/TOTAL_DURATION_VAL/$TOTAL_DURATION/g" "$CONFIG_FILE"
sed -i "s/CONNECTIONS_VAL/$CONNECTIONS/g" "$CONFIG_FILE"
sed -i "s/IO_ITER_VAL/$IO_ITER/g" "$CONFIG_FILE"
sed -i "s/ITER_VAL/$ITER/g" "$CONFIG_FILE"
sed -i "s/JSON_N_VAL/$JSON_N/g" "$CONFIG_FILE"
sed -i "s/IO_SIZE_VAL/$IO_SIZE/g" "$CONFIG_FILE"
sed -i "s/IO_MODE_VAL/$IO_MODE/g" "$CONFIG_FILE"
sed -i "s/TEST_TIME_VAL/$(date -u +%Y-%m-%dT%H:%M:%SZ)/g" "$CONFIG_FILE"

wait_for() {
    name="$1"
    url="$2"
    echo "Waiting for ${name} at ${url}..."
    
    # 先等待网络初始化
    sleep 2
    
    # 尝试使用 wget（主要方法）
    for i in $(seq 1 60); do
        if wget -q -O /dev/null "$url" 2>/dev/null; then
            echo "${name} is ready"
            return 0
        fi
        
        echo "  Attempt $i/60: ${name} not ready yet..."
        sleep 1
    done
    
    echo "WARNING: ${name} not responding after 60s, continuing anyway"
    return 0  # 不中止，继续执行
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

echo ""
echo "=========================================="
echo "Running benchmarks in PARALLEL mode"
echo "=========================================="
echo "Each endpoint test pair runs in parallel"
echo "Total expected time: ~$(echo "$ENDPOINTS" | wc -w) x $DURATION seconds"
echo "=========================================="
echo ""

for endpoint in $ENDPOINTS; do
    path=$(endpoint_url "$endpoint")
    temp_csv_xampp="${TEMP_DIR}/${endpoint}_xampp.csv"
    temp_csv_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.csv"
    temp_json_xampp="${TEMP_DIR}/${endpoint}_xampp.json"
    temp_json_nginx="${TEMP_DIR}/${endpoint}_nginx_multi.json"
    
    echo "Endpoint: $endpoint"
    echo "  [$(date +'%H:%M:%S')] Starting XAMPP and NGINX-Multi in parallel..."
    
    # Start both tests in parallel and save to temporary files
    (
        name="XAMPP (apache)"
        server="xampp"
        url="${URL_XAMPP%/}/$path"
        
        echo "" >&2
        echo "=== ${name} :: ${endpoint} ===" >&2
        
        ab_exit=0
        output=$(ab -l -t "$DURATION" -n "$MAX_REQUESTS" -c "$CONNECTIONS" -q "$url" 2>&1) || ab_exit=$?
        echo "$output" >&2
        if [ "$ab_exit" -ne 0 ]; then
            echo "[WARN] ab exited with code $ab_exit on ${server}/${endpoint}; continuing with parsed partial output." >&2
        fi
        
        parse_ab_output "$output" "$DURATION" "$CONNECTIONS"
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
        output=$(ab -l -t "$DURATION" -n "$MAX_REQUESTS" -c "$CONNECTIONS" -q "$url" 2>&1) || ab_exit=$?
        echo "$output" >&2
        if [ "$ab_exit" -ne 0 ]; then
            echo "[WARN] ab exited with code $ab_exit on ${server}/${endpoint}; continuing with parsed partial output." >&2
        fi
        
        parse_ab_output "$output" "$DURATION" "$CONNECTIONS"
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
    
    # Wait for both to complete
    wait $XAMPP_PID || echo "[WARN] XAMPP process returned non-zero for $endpoint" >&2
    wait $NGINX_PID || echo "[WARN] NGINX process returned non-zero for $endpoint" >&2
    
    # Merge results from temporary files
    [ -f "$temp_csv_xampp" ] && cat "$temp_csv_xampp" >> "$CSV_FILE"
    [ -f "$temp_csv_nginx" ] && cat "$temp_csv_nginx" >> "$CSV_FILE"
    
    if [ -f "$temp_json_xampp" ]; then
        cat "$temp_json_xampp" >> "$JSON_FILE"
        echo "," >> "$JSON_FILE"
    fi
    [ -f "$temp_json_nginx" ] && cat "$temp_json_nginx" >> "$JSON_FILE"
    
    # Clean up temp files
    rm -f "$temp_csv_xampp" "$temp_csv_nginx" "$temp_json_xampp" "$temp_json_nginx"
    
    echo "  [$(date +'%H:%M:%S')] ✓ Both tests completed for $endpoint"
    echo ""
done

# Remove trailing comma from JSON
sed -i '$ s/,$//' "$JSON_FILE"
# Clean up temp directory
rm -rf "$TEMP_DIR"

echo "" >> "$JSON_FILE"
echo "]" >> "$JSON_FILE"
echo "Results saved to ${OUT_DIR}"

