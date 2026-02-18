#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)

assert_gte() {
  actual="$1"
  expected="$2"
  label="$3"
  if [ "$actual" -lt "$expected" ]; then
    echo "[FAIL] $label: expected >= $expected, got $actual" >&2
    exit 1
  fi
}

extract_num() {
  file="$1"
  key="$2"
  awk -F '=' -v k="$key" '$1 ~ k {gsub(/ /, "", $2); print $2; exit}' "$file" | tr -d '\r'
}

extract_nginx_conn() {
  file="$1"
  awk '/worker_connections/ {for(i=1;i<=NF;i++){if($i ~ /^[0-9]+;/){gsub(/;/, "", $i); print $i; exit}}}' "$file" | tr -d '\r'
}

single_conn=$(extract_nginx_conn "$ROOT_DIR/docker/nginx.conf")
multi_conn=$(extract_nginx_conn "$ROOT_DIR/docker/nginx-multi.conf")
assert_gte "$single_conn" 1000 "nginx.conf worker_connections"
assert_gte "$multi_conn" 1000 "nginx-multi.conf worker_connections"

single_children=$(extract_num "$ROOT_DIR/docker/php-fpm.conf" "pm.max_children")
multi_children=$(extract_num "$ROOT_DIR/docker/php-fpm-multi.conf" "pm.max_children")
assert_gte "$single_children" 60 "php-fpm.conf pm.max_children"
assert_gte "$multi_children" 120 "php-fpm-multi.conf pm.max_children"

echo "[PASS] test_high_concurrency_tuning.sh"
