#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

fail() { echo "[FAIL] $1" >&2; exit 1; }

# Nginx single-core config
nginx_conf="$ROOT_DIR/../docker/nginx.conf"
grep -q "worker_rlimit_nofile 8192;" "$nginx_conf" || fail "nginx.conf missing worker_rlimit_nofile"
grep -q "worker_connections 4096" "$nginx_conf" || fail "nginx.conf missing worker_connections"
grep -q "keepalive_requests 10000" "$nginx_conf" || fail "nginx.conf missing keepalive_requests"
grep -q "keepalive_timeout 15" "$nginx_conf" || fail "nginx.conf missing keepalive_timeout"

# Nginx multi-core config
nginx_multi_conf="$ROOT_DIR/../docker/nginx-multi.conf"
grep -q "worker_rlimit_nofile 8192;" "$nginx_multi_conf" || fail "nginx-multi.conf missing worker_rlimit_nofile"
grep -q "worker_connections 4096" "$nginx_multi_conf" || fail "nginx-multi.conf missing worker_connections"
grep -q "keepalive_requests 10000" "$nginx_multi_conf" || fail "nginx-multi.conf missing keepalive_requests"
grep -q "keepalive_timeout 15" "$nginx_multi_conf" || fail "nginx-multi.conf missing keepalive_timeout"

# Apache MPM & keepalive
apache_dockerfile="$ROOT_DIR/../docker/Dockerfile.xampp"
grep -q "MaxRequestWorkers       1200" "$apache_dockerfile" || fail "Dockerfile.xampp missing MaxRequestWorkers 1200"
grep -q "ServerLimit             1200" "$apache_dockerfile" || fail "Dockerfile.xampp missing ServerLimit 1200"
grep -q "MaxKeepAliveRequests 10000" "$apache_dockerfile" || fail "Dockerfile.xampp missing MaxKeepAliveRequests 10000"
grep -q "KeepAliveTimeout 5" "$apache_dockerfile" || fail "Dockerfile.xampp missing KeepAliveTimeout 5"

echo "PASS"
