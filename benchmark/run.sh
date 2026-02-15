#!/bin/sh
set -eu

DURATION=${DURATION:-10s}
CONNECTIONS=${CONNECTIONS:-50}
THREADS=${THREADS:-2}
WARMUP=${WARMUP:-2s}
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
    for i in $(seq 1 30); do
        if wget -q -O /dev/null "$url"; then
            return 0
        fi
        sleep 1
    done
    echo "${name} is not ready after 30s" >&2
    return 1
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

run_wrk() {
    name="$1"
    server="$2"
    endpoint="$3"
    url="$4"
    echo ""
    echo "=== ${name} :: ${endpoint} ==="
    wrk -t"$THREADS" -c"$CONNECTIONS" -d"$WARMUP" "$url" > /dev/null
    output=$(wrk --latency -t"$THREADS" -c"$CONNECTIONS" -d"$DURATION" "$url")
    echo "$output"

    requests_sec=$(printf "%s\n" "$output" | awk '/Requests\/sec/ {print $2; exit}')
    latency_avg=$(printf "%s\n" "$output" | awk '/Latency/ {print $2; exit}')
    transfer_sec=$(printf "%s\n" "$output" | awk '/Transfer\/sec/ {print $2; exit}')
    latency_p50=$(printf "%s\n" "$output" | awk '/Latency Distribution/ {found=1; next} found && $1=="50%" {print $2; exit}')
    latency_p75=$(printf "%s\n" "$output" | awk '/Latency Distribution/ {found=1; next} found && $1=="75%" {print $2; exit}')
    latency_p90=$(printf "%s\n" "$output" | awk '/Latency Distribution/ {found=1; next} found && $1=="90%" {print $2; exit}')
    latency_p99=$(printf "%s\n" "$output" | awk '/Latency Distribution/ {found=1; next} found && $1=="99%" {print $2; exit}')

    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "${timestamp},${server},${endpoint},${requests_sec},${latency_avg},${latency_p50},${latency_p75},${latency_p90},${latency_p99},${transfer_sec}" >> "$CSV_FILE"

    if [ "$JSON_FIRST" -eq 1 ]; then
        JSON_FIRST=0
    else
        echo "," >> "$JSON_FILE"
    fi
    printf "  {\"timestamp\":\"%s\",\"server\":\"%s\",\"endpoint\":\"%s\",\"requests_sec\":%s,\"latency_avg\":\"%s\",\"latency_p50\":\"%s\",\"latency_p75\":\"%s\",\"latency_p90\":\"%s\",\"latency_p99\":\"%s\",\"transfer_sec\":\"%s\"}" \
        "$timestamp" "$server" "$endpoint" "$requests_sec" "$latency_avg" "$latency_p50" "$latency_p75" "$latency_p90" "$latency_p99" "$transfer_sec" >> "$JSON_FILE"

    echo "$output" > "${OUT_DIR}/${server}_${endpoint}.txt"
}

first_endpoint=$(echo "$ENDPOINTS" | awk '{print $1}')
first_path=$(endpoint_url "$first_endpoint")

wait_for "xampp" "${URL_XAMPP%/}/$first_path"
wait_for "nginx" "${URL_NGINX%/}/$first_path"
wait_for "nginx-multi" "${URL_NGINX_MULTI%/}/$first_path"

for endpoint in $ENDPOINTS; do
    path=$(endpoint_url "$endpoint")
    run_wrk "XAMPP (apache)" "xampp" "$endpoint" "${URL_XAMPP%/}/$path"
    run_wrk "NGINX (1 core, 1 process)" "nginx" "$endpoint" "${URL_NGINX%/}/$path"
    run_wrk "NGINX (multi-core, dynamic)" "nginx_multi" "$endpoint" "${URL_NGINX_MULTI%/}/$path"
done

echo "" >> "$JSON_FILE"
echo "]" >> "$JSON_FILE"
echo "Results saved to ${OUT_DIR}"
