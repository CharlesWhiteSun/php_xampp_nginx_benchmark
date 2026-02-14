#!/usr/bin/env pwsh
# 检查压测是否完成的脚本

param(
    [int]$MaxWaitSeconds = 300,
    [int]$CheckIntervalSeconds = 5
)

$ResultsDir = "results"
$MaxIterations = [math]::Floor($MaxWaitSeconds / $CheckIntervalSeconds)
$iteration = 0

Write-Host "🔍 Checking benchmark completion..." -ForegroundColor Cyan
Write-Host "⏱️  Max wait time: ${MaxWaitSeconds}s, Check interval: ${CheckIntervalSeconds}s" -ForegroundColor Gray

function Get-LatestResultDir {
    $dirs = @(Get-ChildItem -Path $ResultsDir -Directory -ErrorAction SilentlyContinue | 
        Where-Object { $_.Name -match '^\d{8}_\d{6}$' } |
        Sort-Object -Property LastWriteTime -Descending)
    if ($dirs.Count -gt 0) {
        return $dirs[0]
    }
    return $null
}

function Check-Results {
    param($Dir)
    
    if (-not (Test-Path "$($Dir.FullName)\results.csv")) {
        return @{ Status = "csv_missing"; Message = "CSV file not created yet" }
    }
    
    $csv = Get-Content "$($Dir.FullName)\results.csv"
    $lines = @($csv | Measure-Object -Line).Lines
    
    if ($lines -le 1) {
        return @{ Status = "csv_empty"; Message = "CSV has headers only" }
    }
    
    # 检查是否有数据记录
    $records = New-Object System.Collections.ArrayList
    foreach ($line in $csv) {
        if ($line -and $line.Trim() -and -not $line.StartsWith("timestamp")) {
            $records.Add($line) > $null
        }
    }
    
    $xamppCount = @($records | Where-Object { $_ -match ',xampp,' }).Count
    $nginxCount = @($records | Where-Object { $_ -match ',nginx,' }).Count
    $nginxMultiCount = @($records | Where-Object { $_ -match ',nginx_multi,' }).Count
    
    $status = @{
        records     = $records.Count
        xampp       = $xamppCount
        nginx       = $nginxCount
        nginx_multi = $nginxMultiCount
    }
    
    if ($nginxMultiCount -eq 0) {
        return @{ Status = "incomplete"; Message = "Missing nginx_multi results"; Data = $status }
    }
    
    # 检查是否包含所有三个端点
    $endpoints = @($records | ForEach-Object { [regex]::Match($_, ',([^,]+)$').Groups[1].Value } | Sort-Object -Unique)
    
    if ($nginxMultiCount -eq 9 -and $xamppCount -eq 9 -and $nginxCount -eq 9) {
        # 3 endpoints × 3 servers = 9 records
        return @{ Status = "complete"; Message = "All tests completed"; Data = $status }
    }
    
    return @{ Status = "in_progress"; Message = "Tests running"; Data = $status }
}

while ($iteration -lt $MaxIterations) {
    $latestDir = Get-LatestResultDir
    
    if ($null -eq $latestDir) {
        Write-Host "⏳ [$iteration/$MaxIterations] Waiting for results directory..." -ForegroundColor Yellow
        Start-Sleep -Seconds $CheckIntervalSeconds
        $iteration++
        continue
    }
    
    $result = Check-Results $latestDir
    $dirName = $latestDir.Name
    
    switch ($result.Status) {
        "csv_missing" {
            Write-Host "⏳ [$iteration/$MaxIterations] $dirName - CSV file not created yet" -ForegroundColor Yellow
        }
        "csv_empty" {
            Write-Host "⏳ [$iteration/$MaxIterations] $dirName - CSV created but empty" -ForegroundColor Yellow
        }
        "in_progress" {
            $data = $result.Data
            Write-Host "🔄 [$iteration/$MaxIterations] $dirName - XAMPP:$($data.xampp) NGINX:$($data.nginx) NGINX-Multi:$($data.nginx_multi)" -ForegroundColor Cyan
        }
        "incomplete" {
            $data = $result.Data
            Write-Host "⏳ [$iteration/$MaxIterations] $dirName - XAMPP:$($data.xampp) NGINX:$($data.nginx) NGINX-Multi:$($data.nginx_multi) (missing multi)" -ForegroundColor Yellow
        }
        "complete" {
            Write-Host "✅ Benchmark complete! Results in: $dirName" -ForegroundColor Green
            $data = $result.Data
            Write-Host "   XAMPP: $($data.xampp) records" -ForegroundColor Green
            Write-Host "   NGINX: $($data.nginx) records" -ForegroundColor Green
            Write-Host "   NGINX-Multi: $($data.nginx_multi) records" -ForegroundColor Green
            return 0
        }
    }
    
    Start-Sleep -Seconds $CheckIntervalSeconds
    $iteration++
}

Write-Host "❌ Timeout! Benchmark did not complete in ${MaxWaitSeconds}s" -ForegroundColor Red
Write-Host "Last status:" -ForegroundColor Gray
$latestDir = Get-LatestResultDir
if ($null -ne $latestDir) {
    Check-Results $latestDir
}
return 1
