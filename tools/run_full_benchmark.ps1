#!/usr/bin/env pwsh
# 完整的压测工作流程

param(
    [int]$TimeoutSeconds = 300
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PHP XAMPP/NGINX Performance Benchmark" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: 停止并清理旧容器
Write-Host "📋 Step 1: Cleaning up old containers..." -ForegroundColor Cyan
docker-compose down --remove-orphans 2>$null | Out-Null
Write-Host "✓ Cleaned up" -ForegroundColor Green
Write-Host ""

# Step 2: 构建镜像
Write-Host "🏗️  Step 2: Building Docker images..." -ForegroundColor Cyan
docker-compose build 2>&1 | Select-String -Pattern "FINISHED|error|Error" | ForEach-Object { Write-Host $_ }
Write-Host "✓ Build completed" -ForegroundColor Green
Write-Host ""

# Step 3: 后台启动容器
Write-Host "🚀 Step 3: Starting containers in background..." -ForegroundColor Cyan
docker-compose up benchmark -d 2>&1
Write-Host "✓ Containers started" -ForegroundColor Green
Write-Host ""

# Step 4: 等待并监控压测进度
Write-Host "⏳ Step 4: Monitoring benchmark progress..." -ForegroundColor Cyan
Write-Host "Expected duration: ~2-3 minutes (3 endpoints × 3 servers × 10s each)" -ForegroundColor Gray
Write-Host ""

$checkScript = Join-Path (Get-Location) "tools/check_benchmark.ps1"
& $checkScript -MaxWaitSeconds $TimeoutSeconds -CheckIntervalSeconds 5

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Benchmark check timed out" -ForegroundColor Yellow
    Write-Host "Checking container status..." -ForegroundColor Gray
    docker-compose ps
    Write-Host ""
    Write-Host "Last logs from benchmark container:" -ForegroundColor Gray
    docker-compose logs benchmark | Select-Object -Last 30
    exit 1
}

Write-Host ""
Write-Host "✓ Benchmark completed successfully" -ForegroundColor Green
Write-Host ""

# Step 5: 生成报告
Write-Host "📊 Step 5: Generating HTML report..." -ForegroundColor Cyan
python tools/generate_report.py
Write-Host ""

# Step 6: 显示结果摘要
Write-Host "📈 Step 6: Results Summary" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

$latestDir = Get-ChildItem -Path "results" -Directory -ErrorAction SilentlyContinue | 
             Where-Object { $_.Name -match '^\d{8}_\d{6}$' } |
             Sort-Object -Property LastWriteTime -Descending |
             Select-Object -First 1

if ($latestDir) {
    $csv = Get-Content "$($latestDir.FullName)\results.csv"
    Write-Host "Results: results/$($latestDir.Name)/results.csv" -ForegroundColor Green
    Write-Host ""
    Write-Host "Preview (first 10 records):" -ForegroundColor Gray
    $csv | Select-Object -First 11 | ForEach-Object { Write-Host $_ }
    Write-Host ""
    
    # 统计摘要
    $records = @($csv | Where-Object { $_ -and $_.Trim() -and -not $_.StartsWith("timestamp") })
    Write-Host "Statistics:" -ForegroundColor Cyan
    Write-Host "  Total records: $($records.Count)" -ForegroundColor Gray
    Write-Host "  XAMPP records: $(@($records | Where-Object { $_ -match ',xampp,' }).Count)" -ForegroundColor Gray
    Write-Host "  NGINX records: $(@($records | Where-Object { $_ -match ',nginx,' }).Count)" -ForegroundColor Gray
    Write-Host "  NGINX-Multi records: $(@($records | Where-Object { $_ -match ',nginx_multi,' }).Count)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ All steps completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📄 Report: reports/report.html" -ForegroundColor Cyan
Write-Host ""
