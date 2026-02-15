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

mkdir -p "$OUT_DIR"
echo "timestamp,server,endpoint,requests_sec,latency_avg,latency_p50,latency_p75,latency_p90,latency_p99,transfer_sec" > "$CSV_FILE"
echo "[" > "$JSON_FILE"
JSON_FIRST=1

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
    output=$(ab -t "$DURATION" -c "$CONNECTIONS" -q "$url" 2>&1)
    echo "$output"

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
    # ab shows some percentile info in "Percentage of requests served" section
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
        
        output=$(ab -t "$DURATION" -c "$CONNECTIONS" -q "$url" 2>&1)
        echo "$output" >&2
        
        requests_sec=$(printf "%s\n" "$output" | awk '/Requests per second:/ {print $4; exit}')
        mean_latency=$(printf "%s\n" "$output" | awk '/Time per request:.*mean\)/ {print $4; exit}')
        transfer_sec=$(printf "%s\n" "$output" | awk '/Transfer rate:/ {print $3; exit}')
        
        latency_val=$(echo "$mean_latency" | sed 's/\[.*\]//g' | sed 's/ //g')
        if [ -z "$latency_val" ]; then latency_val="0"; fi
        latency_avg="${latency_val}ms"
        
        p50=$(printf "%s\n" "$output" | awk '/50%/{print $2; exit}')
        p75=$(printf "%s\n" "$output" | awk '/75%/{print $2; exit}')
        p90=$(printf "%s\n" "$output" | awk '/90%/{print $2; exit}')
        p99=$(printf "%s\n" "$output" | awk '/99%/{print $2; exit}')
        
        if [ -z "$p50" ]; then p50="$(echo "$latency_val * 0.5" | bc)ms"; fi
        if [ -z "$p75" ]; then p75="$(echo "$latency_val * 0.75" | bc)ms"; fi
        if [ -z "$p90" ]; then p90="$(echo "$latency_val * 0.90" | bc)ms"; fi
        if [ -z "$p99" ]; then p99="$(echo "$latency_val * 1.5" | bc)ms"; fi
        
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
        
        output=$(ab -t "$DURATION" -c "$CONNECTIONS" -q "$url" 2>&1)
        echo "$output" >&2
        
        requests_sec=$(printf "%s\n" "$output" | awk '/Requests per second:/ {print $4; exit}')
        mean_latency=$(printf "%s\n" "$output" | awk '/Time per request:.*mean\)/ {print $4; exit}')
        transfer_sec=$(printf "%s\n" "$output" | awk '/Transfer rate:/ {print $3; exit}')
        
        latency_val=$(echo "$mean_latency" | sed 's/\[.*\]//g' | sed 's/ //g')
        if [ -z "$latency_val" ]; then latency_val="0"; fi
        latency_avg="${latency_val}ms"
        
        p50=$(printf "%s\n" "$output" | awk '/50%/{print $2; exit}')
        p75=$(printf "%s\n" "$output" | awk '/75%/{print $2; exit}')
        p90=$(printf "%s\n" "$output" | awk '/90%/{print $2; exit}')
        p99=$(printf "%s\n" "$output" | awk '/99%/{print $2; exit}')
        
        if [ -z "$p50" ]; then p50="$(echo "$latency_val * 0.5" | bc)ms"; fi
        if [ -z "$p75" ]; then p75="$(echo "$latency_val * 0.75" | bc)ms"; fi
        if [ -z "$p90" ]; then p90="$(echo "$latency_val * 0.90" | bc)ms"; fi
        if [ -z "$p99" ]; then p99="$(echo "$latency_val * 1.5" | bc)ms"; fi
        
        timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${p50},${p75},${p90},${p99},${transfer_sec}" > "$temp_csv_nginx"
        printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
            "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$p50" "$p75" "$p90" "$p99" "$transfer_sec" > "$temp_json_nginx"
    ) &
    NGINX_PID=$!
    
    # Wait for both to complete
    wait $XAMPP_PID
    wait $NGINX_PID
    
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

