$ErrorActionPreference = 'Stop'

Write-Host "[TEST] unit: ab parser fallback" -ForegroundColor Cyan
$workspace = (Get-Location).Path
& docker run --rm -v "${workspace}:/workspace" -w /workspace alpine:3.20 sh benchmark/tests/test_ab_parse.sh | Out-Host

Write-Host "[TEST] integration: benchmark output completeness" -ForegroundColor Cyan
$null = docker-compose run --rm -e DURATION=20 -e TOTAL_DURATION=60 -e CONNECTIONS=200 benchmark

$latest = Get-ChildItem .\results -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latest) {
    throw "No results directory found"
}

$csvPath = Join-Path $latest.FullName 'results.csv'
if (-not (Test-Path $csvPath)) {
    throw "results.csv not found: $csvPath"
}

$csvLines = Get-Content $csvPath
foreach ($endpoint in @('cpu.php','json.php','io.php')) {
    if (-not ($csvLines | Where-Object { $_ -match "nginx_multi,$endpoint" })) {
        throw "Missing nginx_multi row for endpoint $endpoint"
    }
}

$badRows = $csvLines | Where-Object { $_ -match 'nginx_multi' -and $_ -match ',0ms,0,0,0,0,' }
if ($badRows) {
    Write-Host "Bad nginx rows:" -ForegroundColor Red
    $badRows | Out-Host
    throw "Found nginx rows with full-zero latency percentile block"
}

Write-Host "[PASS] all tests" -ForegroundColor Green
