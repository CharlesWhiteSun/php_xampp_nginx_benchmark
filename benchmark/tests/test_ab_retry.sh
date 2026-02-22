#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_SH="$ROOT_DIR/run_ab.sh"

FAKE_AB="$ROOT_DIR/tmp_fake_ab_retry.sh"
STATE_FILE="$ROOT_DIR/tmp_fake_state"
cat > "$FAKE_AB" <<'EOF'
#!/bin/sh
STATE_FILE="$1"
if [ ! -f "$STATE_FILE" ]; then
  echo "fail once" >&2
  touch "$STATE_FILE"
  exit 51
fi
cat <<'OUT'
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Time taken for tests:   2.000 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      102400 bytes
Requests per second:    50.00 [#/sec] (mean)
Time per request:       20.000 [ms] (mean)
Time per request:       0.400 [ms] (mean, across all concurrent requests)
Transfer rate:          50.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     0   20   0.0     20      20
Waiting:        0   20   0.0     20      20
Total:          0   20   0.0     20      20
OUT
EOF
chmod +x "$FAKE_AB"

tmp_dir="$ROOT_DIR/tmp_results_test/retry"
rm -rf "$tmp_dir" "$STATE_FILE"
mkdir -p "$tmp_dir"

AB_CMD="$FAKE_AB $STATE_FILE" \
AB_MAX_RETRY=2 \
LIB_AB_PARSE="$ROOT_DIR/lib_ab_parse.sh" \
RESULTS_DIR="$tmp_dir" \
ENDPOINTS="cpu.php" \
URL_XAMPP="http://localhost" \
URL_NGINX_MULTI="http://localhost" \
WAIT_FOR_SKIP=1 \
ENDPOINT_SCHEDULE=sequential \
CPU_DURATION=2 \
JSON_DURATION=2 \
IO_DURATION=2 \
CPU_CONNECTIONS=1 \
JSON_CONNECTIONS=1 \
IO_CONNECTIONS=1 \
DURATION=2 \
MAX_REQUESTS=100 \
ITER=1 \
JSON_N=1 \
IO_SIZE=1 \
IO_ITER=1 \
IO_MODE=memory \
/bin/sh "$RUN_SH" >/dev/null 2>&1 || true

latest_dir=$(ls -1t "$tmp_dir" 2>/dev/null | head -n1 || true)
if [ -z "$latest_dir" ]; then
  echo "No run output found" >&2
  rm -rf "$tmp_dir" "$STATE_FILE" "$FAKE_AB"
  exit 1
fi

csv="$tmp_dir/$latest_dir/results.csv"
log="$tmp_dir/$latest_dir/xampp_cpu.php.log"

if ! grep -q "retrying" "$log"; then
  echo "Retry marker not found in log" >&2
  rm -rf "$tmp_dir" "$STATE_FILE" "$FAKE_AB"
  exit 1
fi

if ! awk -F, 'NR==2 {exit ($4 > 0 ? 0 : 1)}' "$csv"; then
  echo "Requests/sec not recovered after retry" >&2
  rm -rf "$tmp_dir" "$STATE_FILE" "$FAKE_AB"
  exit 1
fi

rm -rf "$tmp_dir" "$STATE_FILE" "$FAKE_AB"
echo "PASS"
