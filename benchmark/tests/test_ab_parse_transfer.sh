#!/bin/sh
set -eu

# shellcheck source=../lib_ab_parse.sh
. "$(cd "$(dirname "$0")/.." && pwd)/lib_ab_parse.sh"

sample_output=$(cat <<'EOF'
This is ApacheBench, Version 2.3 <$Revision: 1923142 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking example (be patient).....done

Time taken for tests:   2.000 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      102400 bytes
HTML transferred:       102400 bytes
Requests per second:    50.00 [#/sec] (mean)
Time per request:       20.000 [ms] (mean)
Time per request:       0.400 [ms] (mean, across all concurrent requests)

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     0   20   0.0     20      20
Waiting:        0   20   0.0     20      20
Total:          0   20   0.0     20      20
EOF
)

parse_ab_output "$sample_output" 2 5

if [ "$PARSED_TRANSFER_SEC" != "50.00" ]; then
  echo "Expected transfer_sec=50.00, got $PARSED_TRANSFER_SEC" >&2
  exit 1
fi

echo "PASS"
