#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SCRIPT_DIR/../lib_ab_parse.sh"

assert_eq() {
  expected="$1"
  actual="$2"
  msg="$3"
  if [ "$expected" != "$actual" ]; then
    echo "[FAIL] $msg: expected '$expected', got '$actual'" >&2
    exit 1
  fi
}

assert_not_zero_ms() {
  value="$1"
  msg="$2"
  if [ "$value" = "0ms" ] || [ -z "$value" ]; then
    echo "[FAIL] $msg: got '$value'" >&2
    exit 1
  fi
}

full_output='Requests per second:    1538.13 [#/sec] (mean)
Time per request:       130.028 [ms] (mean)
Transfer rate:          403.97 [Kbytes/sec] received

Percentage of the requests served within a certain time (ms)
  50%    115
  75%    142
  90%    172
  99%    312'

parse_ab_output "$full_output" 40 200
assert_eq "1538.13" "$PARSED_REQUESTS_SEC" "full parse requests/sec"
assert_eq "130.028ms" "$PARSED_LATENCY_AVG" "full parse latency"
assert_eq "115" "$PARSED_P50" "full parse p50"
assert_eq "312" "$PARSED_P99" "full parse p99"

partial_output='Benchmarking nginx-multi (be patient)...apr_socket_recv: Connection reset by peer (104)
Total of 43300 requests completed'

parse_ab_output "$partial_output" 40 200
assert_eq "1082.50" "$PARSED_REQUESTS_SEC" "partial parse requests/sec fallback"
assert_not_zero_ms "$PARSED_LATENCY_AVG" "partial parse latency fallback"
assert_eq "0" "$PARSED_TRANSFER_SEC" "partial parse transfer fallback"
assert_eq "166" "$PARSED_P50" "partial parse p50 estimated"
assert_eq "277" "$PARSED_P99" "partial parse p99 estimated"

echo "[PASS] test_ab_parse.sh"
