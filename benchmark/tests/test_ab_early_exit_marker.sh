#!/bin/sh
set -eu

# This test simulates ab 提早結束：我們用假的 ab 指令快速結束，檢查 run_ab.sh 是否產生 warning 標記。

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_SH="$ROOT_DIR/run_ab.sh"

FAKE_AB="$ROOT_DIR/tmp_fake_ab.sh"
cat > "$FAKE_AB" <<'EOF'
#!/bin/sh
echo "This is ApacheBench, Version 2.3"
echo "Time taken for tests:   1.000 seconds"
echo "Complete requests:      10"
echo "Total transferred:      1000 bytes"
echo "Requests per second:    10.00 [#/sec] (mean)"
EOF
chmod +x "$FAKE_AB"

OUT_BASE="$ROOT_DIR/tmp_results_test/early_exit"
rm -rf "$OUT_BASE"
mkdir -p "$OUT_BASE"

AB_CMD="$FAKE_AB" \
LIB_AB_PARSE="$ROOT_DIR/lib_ab_parse.sh" \
RESULTS_DIR="$OUT_BASE" \
ENDPOINTS="cpu.php" \
URL_XAMPP="http://localhost" \
URL_NGINX_MULTI="http://localhost" \
WAIT_FOR_SKIP=1 \
ENDPOINT_SCHEDULE=sequential \
CPU_DURATION=5 \
JSON_DURATION=5 \
IO_DURATION=5 \
CPU_CONNECTIONS=1 \
JSON_CONNECTIONS=1 \
IO_CONNECTIONS=1 \
DURATION=5 \
MAX_REQUESTS=100 \
ITER=1 \
JSON_N=1 \
IO_SIZE=1 \
IO_ITER=1 \
IO_MODE=memory \
/bin/sh "$RUN_SH" >/dev/null 2>&1 || true

latest_dir=$(ls -1t "$OUT_BASE" 2>/dev/null | head -n1 || true)
if [ -z "$latest_dir" ]; then
  echo "No run output found" >&2
  rm -rf "$OUT_BASE" "$FAKE_AB"
  exit 1
fi

log_file="$OUT_BASE/$latest_dir"/xampp_cpu.php.log
if ! grep -q "finished in" "$log_file" 2>/dev/null; then
  echo "Expected early-exit warning log not found" >&2
  rm -rf "$OUT_BASE" "$FAKE_AB"
  exit 1
fi

rm -rf "$OUT_BASE" "$FAKE_AB"
echo "PASS"