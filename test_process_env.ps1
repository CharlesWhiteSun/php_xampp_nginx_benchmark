# Test PowerShell Process with environment variables

$startTime = Get-Date
$duration = 180  # 3 minutes for testing
$connections = 50

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Testing Duration: $duration seconds" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "docker-compose"
$processInfo.Arguments = "run --rm -e `"DURATION=$duration`" -e `"CONNECTIONS=$connections`" benchmark bash ./benchmark/test_env.sh"
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.CreateNoWindow = $true

Write-Host "Running: docker-compose run --rm -e DURATION=$duration -e CONNECTIONS=$connections benchmark bash ./benchmark/test_env.sh" -ForegroundColor Yellow
Write-Host ""

$process = [System.Diagnostics.Process]::Start($processInfo)

# Monitor progress
$lastUpdate = Get-Date
while (-not $process.HasExited) {
    $currentTime = Get-Date
    $elapsedSeconds = [int]($currentTime - $startTime).TotalSeconds
    
    if (($currentTime - $lastUpdate).TotalSeconds -ge 1) {
        $percentage = [math]::Min(100, ($elapsedSeconds / $duration) * 100)
        $barLength = 30
        $filledLength = [math]::Round(($percentage / 100) * $barLength)
        $emptyLength = $barLength - $filledLength
        
        $bar = "[" + ("=" * $filledLength) + (" " * $emptyLength) + "]"
        $remaining = [math]::Max(0, $duration - $elapsedSeconds)
        
        Write-Host "`r  Progress: $bar $([math]::Round($percentage))% | Elapsed: $($elapsedSeconds)s | Remaining: $($remaining)s" -ForegroundColor Cyan -NoNewline
        
        $lastUpdate = $currentTime
    }
    
    Start-Sleep -Milliseconds 100
}

# Read output
$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()

$endTime = Get-Date
$elapsed = $endTime - $startTime

Write-Host ""
Write-Host ""
Write-Host "[SUCCESS] Test completed!" -ForegroundColor Green
Write-Host "   Total Duration: $([math]::Round($elapsed.TotalSeconds)) seconds" -ForegroundColor Green
Write-Host ""
Write-Host "Output:" -ForegroundColor Cyan
Write-Host $output
if ($errors) {
    Write-Host "Errors:" -ForegroundColor Yellow
    Write-Host $errors
}
