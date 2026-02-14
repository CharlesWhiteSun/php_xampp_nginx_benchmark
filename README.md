# PHP XAMPP vs NGINX single-thread benchmark

This repo compares PHP performance between:
- XAMPP-like Apache+PHP via `php:8.1-apache`
- NGINX with PHP-FPM using a single worker/process

## Quick start

Build and run both servers:

```bash
docker compose up -d --build xampp nginx
```

If you add or edit PHP files, they are mounted into the containers automatically.

Check endpoints on host:
- http://localhost:8081/index.php
- http://localhost:8082/index.php

Workloads:
- http://localhost:8081/cpu.php?n=10000
- http://localhost:8081/json.php?n=2000
- http://localhost:8081/io.php?size=32768&iter=50

Run the benchmark from the benchmark container:

```bash
docker compose run --rm benchmark
```

Benchmark results are written to `./results/<timestamp>/`:
- `results.csv`
- `results.json`
- raw wrk output per server/endpoint

Note: The benchmark captures latency percentiles (P50/P75/P90/P99). It uses a source-built wrk to ensure percentile output is available. Rebuild the benchmark image if you change it.

## Report

Generate a visual report (HTML) from the latest results:

```bash
python tools/generate_report.py
```

The report is saved to `./reports/report.html`.

## Tuning

You can override benchmark parameters:

```bash
docker compose run --rm \
  -e DURATION=20s \
  -e CONNECTIONS=100 \
  -e THREADS=4 \
  -e ITER=20000 \
  -e JSON_N=4000 \
  -e IO_SIZE=65536 \
  -e IO_ITER=100 \
  benchmark
```

## Notes

- NGINX is configured with `worker_processes 1` and PHP-FPM with `pm.max_children 1`.
- Workloads live in [app/cpu.php](app/cpu.php), [app/json.php](app/json.php), [app/io.php](app/io.php).
