#Requires -Version 5.0
# Test environment variable passing to docker-compose

$duration = 60
$connections = 50

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Testing Environment Variable Passing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Duration: $duration seconds" -ForegroundColor Yellow
Write-Host "Connections: $connections" -ForegroundColor Yellow
Write-Host ""

# Build arguments array (same way as start_benchmark.ps1)
$args = @(
    "run", "--rm",
    "-e", "DURATION=$duration",
    "-e", "CONNECTIONS=$connections",
    "benchmark",
    "bash",
    "-c", "echo 'DURATION='`$DURATION; echo 'CONNECTIONS='`$CONNECTIONS"
)

Write-Host "Docker command:" -ForegroundColor Cyan
Write-Host "docker-compose $($args -join ' ')" -ForegroundColor Gray
Write-Host ""

# Create process
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "docker-compose"
$processInfo.Arguments = [System.String]::Join(" ", $args)
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.CreateNoWindow = $true

$process = [System.Diagnostics.Process]::Start($processInfo)
$process.WaitForExit()

$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()

Write-Host "Output:" -ForegroundColor Cyan
Write-Host $output
if ($errors) {
    Write-Host "Errors:" -ForegroundColor Yellow
    Write-Host $errors
}

Write-Host ""
Write-Host "Process Exit Code: $($process.ExitCode)" -ForegroundColor Gray
