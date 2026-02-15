#!/bin/sh
set -eu

DURATION=${DURATION:-10}
CONNECTIONS=${CONNECTIONS:-50}
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
TEMP_DIR="${OUT_DIR}/temp"

mkdir -p "$OUT_DIR" "$TEMP_DIR"
echo "timestamp,server,endpoint,requests_sec,latency_avg,latency_p50,latency_p75,latency_p90,latency_p99,transfer_sec" > "$CSV_FILE"
echo "[" > "$JSON_FILE"

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
    return 0
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
    output_file="$5"
    csv_temp_file="$6"
    json_temp_file="$7"
    
    echo "=== ${name} :: ${endpoint} ===" | tee "$output_file"
    
    # Run ab test with full output
    output=$(ab -t "$DURATION" -c "$CONNECTIONS" -q "$url" 2>&1)
    echo "$output" | tee -a "$output_file"

    # Extract metrics from ab output
    requests_sec=$(printf "%s\n" "$output" | awk '/Requests per second:/ {print $4; exit}')
    mean_latency=$(printf "%s\n" "$output" | awk '/Time per request:.*mean\)/ {print $4; exit}')
    transfer_sec=$(printf "%s\n" "$output" | awk '/Transfer rate:/ {print $3; exit}')
    
    # Parse latency string (e.g., "33.016 [ms]" or "33.016")
    latency_val=$(echo "$mean_latency" | sed 's/\[.*\]//g' | sed 's/ //g')
    if [ -z "$latency_val" ]; then
        latency_val="0"
    fi
    latency_avg="${latency_val}ms"
    
    # For ab, we don't have percentiles, so approximate them
    p50=$(printf "%s\n" "$output" | awk '/50%/{print $2; exit}')
    p75=$(printf "%s\n" "$output" | awk '/75%/{print $2; exit}')
    p90=$(printf "%s\n" "$output" | awk '/90%/{print $2; exit}')
    p99=$(printf "%s\n" "$output" | awk '/99%/{print $2; exit}')
    
    # Fallback to approximations if percentiles not found
    if [ -z "$p50" ]; then p50="$(echo "$latency_val * 0.5" | bc)ms"; fi
    if [ -z "$p75" ]; then p75="$(echo "$latency_val * 0.75" | bc)ms"; fi
    if [ -z "$p90" ]; then p90="$(echo "$latency_val * 0.90" | bc)ms"; fi
    if [ -z "$p99" ]; then p99="$(echo "$latency_val * 1.5" | bc)ms"; fi
    
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Write to temp CSV file (one line per result)
    echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${p50},${p75},${p90},${p99},${transfer_sec}" >> "$csv_temp_file"
    
    # Write to temp JSON file (JSON object)
    printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
        "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$p50" "$p75" "$p90" "$p99" "$transfer_sec" >> "$json_temp_file"
}

first_endpoint=$(echo "$ENDPOINTS" | awk '{print $1}')
first_path=$(endpoint_url "$first_endpoint")

wait_for "xampp" "${URL_XAMPP%/}/$first_path"
wait_for "nginx-multi" "${URL_NGINX_MULTI%/}/$first_path"

echo ""
echo "=========================================="
echo "Starting PARALLEL benchmark tests"
echo "=========================================="
echo ""

# 並行執行每個端點的壓測
for endpoint in $ENDPOINTS; do
    path=$(endpoint_url "$endpoint")
    
    # Create temporary files for this endpoint batch
    CSV_TEMP="${TEMP_DIR}/${endpoint}.csv"
    JSON_TEMP="${TEMP_DIR}/${endpoint}.json"
    
    touch "$CSV_TEMP" "$JSON_TEMP"
    
    echo "Endpoint: $endpoint"
    echo "  Starting XAMPP and NGINX-Multi in parallel..."
    
    # Start two tests in parallel
    run_ab "XAMPP (apache)" "xampp" "$endpoint" "${URL_XAMPP%/}/$path" "${OUT_DIR}/xampp_${endpoint}.txt" "$CSV_TEMP.xampp" "$JSON_TEMP.xampp" &
    XAMPP_PID=$!
    
    run_ab "NGINX (multi-core, dynamic)" "nginx_multi" "$endpoint" "${URL_NGINX_MULTI%/}/$path" "${OUT_DIR}/nginx_multi_${endpoint}.txt" "$CSV_TEMP.nginx" "$JSON_TEMP.nginx" &
    NGINX_PID=$!
    
    # Wait for both to complete
    wait $XAMPP_PID
    wait $NGINX_PID
    
    echo "  ✓ Both tests completed for $endpoint"
    echo ""
done

echo "=========================================="
echo "Merging results..."
echo "=========================================="

# Merge all CSV files
for endpoint in $ENDPOINTS; do
    CSV_TEMP="${TEMP_DIR}/${endpoint}"
    if [ -f "$CSV_TEMP.xampp" ]; then
        cat "$CSV_TEMP.xampp" >> "$CSV_FILE"
    fi
    if [ -f "$CSV_TEMP.nginx" ]; then
        cat "$CSV_TEMP.nginx" >> "$CSV_FILE"
    fi
done

# Merge all JSON files
FIRST_JSON=1
for endpoint in $ENDPOINTS; do
    JSON_TEMP="${TEMP_DIR}/${endpoint}"
    
    if [ "$FIRST_JSON" -eq 1 ]; then
        FIRST_JSON=0
    else
        echo "," >> "$JSON_FILE"
    fi
    
    if [ -f "$JSON_TEMP.xampp" ]; then
        cat "$JSON_TEMP.xampp" >> "$JSON_FILE"
        if [ -f "$JSON_TEMP.nginx" ]; then
            echo "," >> "$JSON_FILE"
        fi
    fi
    
    if [ -f "$JSON_TEMP.nginx" ]; then
        cat "$JSON_TEMP.nginx" >> "$JSON_FILE"
        if [ "$endpoint" != "$(echo "$ENDPOINTS" | awk '{print $NF}')" ] || [ -f "$JSON_TEMP.nginx" ]; then
            :  # No trailing comma needed after last entry
        fi
    fi
done

echo "" >> "$JSON_FILE"
echo "]" >> "$JSON_FILE"

# Cleanup temp files
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "Results saved to ${OUT_DIR}"
echo "=========================================="
echo "Summary:"
echo "  CSV: $CSV_FILE"
echo "  JSON: $JSON_FILE"
echo "=========================================="
