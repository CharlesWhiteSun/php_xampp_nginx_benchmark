#Requires -Version 5.0
# PHP XAMPP NGINX Benchmark - Interactive Menu Configuration

Clear-Host

# Configuration presets
$Config1_Name = "Quick Test (3 minutes)"
$Config1_Duration = 180
$Config1_Connections = 50
$Config1_Description = "Fast verification during development"

$Config2_Name = "Standard Test (10 minutes) [RECOMMENDED]"
$Config2_Duration = 600
$Config2_Connections = 100
$Config2_Description = "Daily benchmark testing, most balanced"

$Config3_Name = "Long-term Test (30 minutes)"
$Config3_Duration = 1800
$Config3_Connections = 150
$Config3_Description = "Observe long-term stability and memory leaks"

$Config4_Name = "Ultra-long Test (1 hour)"
$Config4_Duration = 3600
$Config4_Connections = 200
$Config4_Description = "Extreme stress test, capacity planning"

$Config5_Name = "Custom Parameters"
$Config5_Description = "Customize test time and connection count"

function Show-Header {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   PHP XAMPP NGINX Benchmark Tool" -ForegroundColor Cyan
    Write-Host "   Interactive Configuration Menu" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    Write-Host "Select Benchmark Mode:" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "  1. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config1_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config1_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  2. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config2_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config2_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  3. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config3_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config3_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  4. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config4_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config4_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  5. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config5_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config5_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  0. " -ForegroundColor Magenta -NoNewline
    Write-Host "Exit" -ForegroundColor Magenta
    Write-Host ""
}


function Get-CustomConfig {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Custom Configuration" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    do {
        Write-Host "Enter test duration (seconds, min: 10): " -ForegroundColor Cyan -NoNewline
        $duration = Read-Host
        if ($duration -notmatch '^\d+$' -or [int]$duration -lt 10) {
            Write-Host "[ERROR] Please enter a number greater than 10" -ForegroundColor Red
            continue
        }
        break
    } while ($true)
    
    do {
        Write-Host "Enter concurrent connections (min: 1): " -ForegroundColor Cyan -NoNewline
        $connections = Read-Host
        if ($connections -notmatch '^\d+$' -or [int]$connections -lt 1) {
            Write-Host "[ERROR] Please enter a number greater than 0" -ForegroundColor Red
            continue
        }
        break
    } while ($true)
    
    return @{
        Name        = "Custom Configuration"
        Duration    = [int]$duration
        Connections = [int]$connections
    }
}


function Show-ConfigSummary {
    param(
        [hashtable]$Config,
        [string]$ConfigName,
        [int]$EndpointCount
    )

    $perEndpointDuration = [math]::Max(1, [int][math]::Ceiling($Config.Duration / [double][math]::Max(1, $EndpointCount)))
    $effectiveTotalDuration = $perEndpointDuration * [math]::Max(1, $EndpointCount)
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Configuration Summary" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Selected Mode: " -ForegroundColor White -NoNewline
    Write-Host "$ConfigName" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Parameters:" -ForegroundColor White
    Write-Host "    * Total Duration: $effectiveTotalDuration seconds ($([math]::Round($effectiveTotalDuration/60, 1)) minutes)" -ForegroundColor White
    Write-Host "    * Per Endpoint Duration: $perEndpointDuration seconds" -ForegroundColor Gray
    Write-Host "    * Connections: $($Config.Connections)" -ForegroundColor White
    Write-Host ""
}

function Show-ProgressTimeline {
    param(
        [int]$TotalSeconds,
        [int]$ElapsedSeconds
    )
    
    $percentage = [math]::Min(100, ($ElapsedSeconds / $TotalSeconds) * 100)
    $barLength = 30
    $filledLength = [math]::Round(($percentage / 100) * $barLength)
    $emptyLength = $barLength - $filledLength
    
    $bar = "[" + ("=" * $filledLength) + (" " * $emptyLength) + "]"
    $remaining = $TotalSeconds - $ElapsedSeconds
    
    Write-Host ""
    Write-Host "  Progress: $bar $([math]::Round($percentage))%" -ForegroundColor Cyan
    Write-Host "  Time remaining: $($remaining)s | Elapsed: $($ElapsedSeconds)s" -ForegroundColor Gray
}

function Update-BenchmarkProgress {
    param(
        [int]$ElapsedSeconds,
        [int]$EstimatedTotalSeconds,
        [switch]$Completed
    )

    $displayElapsed = [math]::Min($ElapsedSeconds, $EstimatedTotalSeconds)
    $remaining = [math]::Max(0, $EstimatedTotalSeconds - $displayElapsed)
    if ($Completed) {
        $percentage = 100
    }
    else {
        $percentage = [math]::Min(99, [int](($displayElapsed * 100) / [math]::Max(1, $EstimatedTotalSeconds)))
    }
    $barLength = 30
    $filledLength = [math]::Round(($percentage / 100) * $barLength)
    $emptyLength = $barLength - $filledLength
    $bar = "[" + ("=" * $filledLength) + (" " * $emptyLength) + "]"
    $status = if ($Completed) {
        "  Progress: [==============================] 100% | Finalizing..."
    }
    elseif ($displayElapsed -ge $EstimatedTotalSeconds) {
        "  Progress: [============================= ] 99% | Finalizing..."
    }
    else {
        "  Progress: $bar $percentage% | Elapsed: ${ElapsedSeconds}s | Remaining: ${remaining}s"
    }

    if ($script:ProgressUseInline) {
        try {
            $width = [math]::Max(60, $Host.UI.RawUI.WindowSize.Width - 1)
            $coords = New-Object System.Management.Automation.Host.Coordinates 0, $script:ProgressLineY
            $Host.UI.RawUI.CursorPosition = $coords
            $renderText = $status
            if ($renderText.Length -gt $width) {
                $renderText = $renderText.Substring(0, $width)
            }
            Write-Host ($renderText.PadRight($width)) -NoNewline -ForegroundColor Cyan
            if ($Completed) {
                Write-Host ""
            }
            return
        }
        catch {
            $script:ProgressUseInline = $false
            $script:LastFallbackSecond = -1
        }
    }

    if ($script:ProgressUseCarriageReturn) {
        try {
            $width = if ($script:ProgressLineWidth -gt 0) { $script:ProgressLineWidth } else { 120 }
            $renderText = $status
            if ($renderText.Length -gt $width) {
                $renderText = $renderText.Substring(0, $width)
            }
            Write-Host ("`r" + $renderText.PadRight($width)) -NoNewline -ForegroundColor Cyan
            if ($Completed) {
                Write-Host ""
            }
            return
        }
        catch {
            $script:ProgressUseCarriageReturn = $false
            $script:LastFallbackSecond = -1
        }
    }

    if ($Completed) {
        Write-Host $status -ForegroundColor Cyan
        return
    }

    if ($ElapsedSeconds -ne $script:LastFallbackSecond -and (($ElapsedSeconds % 5) -eq 0)) {
        Write-Host $status -ForegroundColor Cyan
        $script:LastFallbackSecond = $ElapsedSeconds
    }
}

function Test-DockerReadiness {
    $composeCommand = Get-Command docker-compose -ErrorAction SilentlyContinue
    if (-not $composeCommand) {
        Write-Host "" 
        Write-Host "[ERROR] docker-compose command not found." -ForegroundColor Red
        Write-Host "   Please install Docker Desktop and ensure docker-compose is available in PATH." -ForegroundColor Yellow
        Write-Host "" 
        return $false
    }

    $dockerCommand = Get-Command docker -ErrorAction SilentlyContinue
    if (-not $dockerCommand) {
        Write-Host "" 
        Write-Host "[ERROR] docker command not found." -ForegroundColor Red
        Write-Host "   Please install Docker Desktop and add docker to PATH." -ForegroundColor Yellow
        Write-Host "" 
        return $false
    }

    $dockerInfoOutput = & docker info 2>&1
    $dockerExitCode = $LASTEXITCODE

    if ($dockerExitCode -ne 0) {
        Write-Host "" 
        Write-Host "[ERROR] Docker engine is not available." -ForegroundColor Red
        Write-Host "   Please start Docker Desktop and wait until status is Running, then retry." -ForegroundColor Yellow
        if ($dockerInfoOutput) {
            $firstLine = (($dockerInfoOutput | Select-Object -First 1) -join "").Trim()
            if (-not [string]::IsNullOrWhiteSpace($firstLine)) {
                Write-Host "   Details: $firstLine" -ForegroundColor DarkYellow
            }
        }
        Write-Host "" 
        return $false
    }

    return $true
}

function Start-Benchmark {
    param(
        [hashtable]$Config,
        [string]$ConfigName
    )

    if (-not (Test-DockerReadiness)) {
        return $false
    }

    $endpointCount = 3
    $perEndpointDuration = [math]::Max(1, [int][math]::Ceiling($Config.Duration / [double]$endpointCount))
    $effectiveTotalDuration = $perEndpointDuration * $endpointCount
    
    Show-ConfigSummary -Config $Config -ConfigName $ConfigName -EndpointCount $endpointCount
    
    Write-Host "Confirm to start? (Y/N) [Press Enter for Yes]: " -ForegroundColor Cyan -NoNewline
    $confirm = Read-Host

    $script:ProgressUseInline = $false
    $script:ProgressUseCarriageReturn = $false
    $script:ProgressLineY = 0
    $script:ProgressLineWidth = 120
    $script:LastFallbackSecond = -1
    try {
        if (-not [Console]::IsOutputRedirected) {
            $script:ProgressUseCarriageReturn = $true
        }

        if ($Host.UI -and $Host.UI.RawUI) {
            $script:ProgressLineWidth = [math]::Max(60, $Host.UI.RawUI.WindowSize.Width - 1)
        }

        if ($Host.Name -eq "ConsoleHost" -and -not [Console]::IsInputRedirected -and -not [Console]::IsOutputRedirected) {
            $script:ProgressLineY = $Host.UI.RawUI.CursorPosition.Y
            $script:ProgressUseInline = $true
        }
    }
    catch {
        $script:ProgressUseInline = $false
    }
    
    # If user presses Enter (empty input) or types Y/y, proceed. Only N/n cancels.
    if ($confirm -eq "N" -or $confirm -eq "n") {
        Write-Host ""
        Write-Host "[CANCELLED] Exiting..." -ForegroundColor Yellow
        Write-Host ""
        exit 0
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Benchmarking in progress..." -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    $startTime = Get-Date
    $estimatedEndTime = $startTime.AddSeconds($Config.Duration)
    
    try {
        # Create temp file for benchmark output
        $outputFile = "$env:TEMP\benchmark_$([guid]::NewGuid()).txt"
        
        # Start benchmark in background and capture process output to file
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "cmd.exe"
        # Use array for arguments to properly handle quotes and spaces
        $args = @(
            "run", "--rm",
            "-e", "DURATION=$perEndpointDuration",
            "-e", "CONNECTIONS=$($Config.Connections)",
            "benchmark"
        )
        $composeCommand = "docker-compose " + ([System.String]::Join(" ", $args)) + " > `"$outputFile`" 2>&1"
        $processInfo.Arguments = "/c $composeCommand"
        $processInfo.UseShellExecute = $false
        # Output is redirected by cmd, so no stream redirection needed here.
        $processInfo.RedirectStandardOutput = $false
        $processInfo.RedirectStandardError = $false
        $processInfo.CreateNoWindow = $true
        
        $process = [System.Diagnostics.Process]::Start($processInfo)
        
        # Progress bar with countdown (shared logic for all menu options).
        # run_ab.sh runs 3 endpoints sequentially (cpu/json/io), each for DURATION seconds.
        # DURATION here is per-endpoint duration, derived from selected total duration.
        $estimatedTotalSeconds = [math]::Max(1, $effectiveTotalDuration)
        Write-Host ""
        
        while (-not $process.HasExited) {
            $currentTime = Get-Date
            $elapsedSeconds = [int]($currentTime - $startTime).TotalSeconds
            Update-BenchmarkProgress -ElapsedSeconds $elapsedSeconds -EstimatedTotalSeconds $estimatedTotalSeconds
            
            Start-Sleep -Milliseconds 1000
        }

        Update-BenchmarkProgress -ElapsedSeconds $estimatedTotalSeconds -EstimatedTotalSeconds $estimatedTotalSeconds -Completed
        
        # Wait for process to complete
        $process.WaitForExit()
        
        $endTime = Get-Date
        $elapsed = $endTime - $startTime
        $exitCode = $process.ExitCode
        $minExpectedSeconds = [math]::Max(5, [int]($estimatedTotalSeconds * 0.9))
        $completedEarly = $elapsed.TotalSeconds -lt $minExpectedSeconds
        
        if ($exitCode -ne 0) {
            Write-Host "" 
            Write-Host "[ERROR] Benchmark execution failed." -ForegroundColor Red
            Write-Host "   Exit Code: $exitCode" -ForegroundColor Red
            Write-Host "   Elapsed: $([math]::Round($elapsed.TotalSeconds))s (estimated around ${estimatedTotalSeconds}s)" -ForegroundColor Red
            if (Test-Path $outputFile) {
                Write-Host "   Log file: $outputFile" -ForegroundColor Yellow
                Write-Host "   Hint: Open the log file and check the first error line for root cause." -ForegroundColor DarkYellow
            }
            Write-Host ""
            return $false
        }

        if ($completedEarly) {
            Write-Host "" 
            Write-Host "[WARNING] Benchmark finished earlier than estimated, but completed successfully." -ForegroundColor Yellow
            Write-Host "   Exit Code: $exitCode" -ForegroundColor Yellow
            Write-Host "   Elapsed: $([math]::Round($elapsed.TotalSeconds))s (estimated around ${estimatedTotalSeconds}s)" -ForegroundColor Yellow
            Write-Host "   This is not a failure." -ForegroundColor Green
            Write-Host "   Possible reason: ApacheBench reached request limits before timeout." -ForegroundColor DarkYellow
            Write-Host ""
        }
        
        Write-Host ""
        Write-Host ""
        Write-Host "[SUCCESS] Benchmark completed!" -ForegroundColor Green
        Write-Host "   Total Duration: $([math]::Round($elapsed.TotalSeconds)) seconds ($([math]::Round($elapsed.TotalMinutes, 2)) minutes)" -ForegroundColor Green
        Write-Host ""
        
        # Clean up
        if (Test-Path $outputFile) {
            Remove-Item $outputFile -ErrorAction SilentlyContinue
        }
        
        return $true
    }
    catch {
        Write-Host ""
        Write-Host "[ERROR] Benchmark failed: $_" -ForegroundColor Red
        Write-Host ""
        exit 1
    }
}

function Generate-Report {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Generating Report..." -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        python tools/generate_report.py
        Write-Host ""
        Write-Host "[SUCCESS] Report generated!" -ForegroundColor Green
        Write-Host "   Location: reports/report.html" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Open report in browser? (Y/N) [Press Enter for Yes]: " -ForegroundColor Cyan -NoNewline
        $openReport = Read-Host
        
        # If user presses Enter (empty input) or types Y/y, open the report
        if ($openReport -ne "N" -and $openReport -ne "n") {
            Start-Process "reports/report.html"
            Write-Host "[INFO] Opening report in browser..." -ForegroundColor Green
        }
    }
    catch {
        Write-Host "[ERROR] Failed to generate report: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

function Show-LatestResults {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Latest Results" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $latest = Get-ChildItem results/ -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($latest) {
        Write-Host "  Latest directory: $($latest.Name)" -ForegroundColor White
        Write-Host "  Location: results/$($latest.Name)/" -ForegroundColor White
        Write-Host ""
        Write-Host "  Files:" -ForegroundColor White
        Get-ChildItem $latest.FullName | ForEach-Object {
            $size = if ($_.PSIsContainer) { "-" } else { "$([math]::Round($_.Length/1KB, 1)) KB" }
            Write-Host "    * $($_.Name) ($size)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
}

Show-Header

do {
    Show-Menu
    
    $choice = Read-Host "Select option (1-5, 0 to exit)"
    
    switch ($choice) {
        "1" {
            if (Start-Benchmark -Config @{Duration = $Config1_Duration; Connections = $Config1_Connections} -ConfigName $Config1_Name) {
                Generate-Report
                Show-LatestResults
            }
        }
        "2" {
            if (Start-Benchmark -Config @{Duration = $Config2_Duration; Connections = $Config2_Connections} -ConfigName $Config2_Name) {
                Generate-Report
                Show-LatestResults
            }
        }
        "3" {
            if (Start-Benchmark -Config @{Duration = $Config3_Duration; Connections = $Config3_Connections} -ConfigName $Config3_Name) {
                Generate-Report
                Show-LatestResults
            }
        }
        "4" {
            if (Start-Benchmark -Config @{Duration = $Config4_Duration; Connections = $Config4_Connections} -ConfigName $Config4_Name) {
                Generate-Report
                Show-LatestResults
            }
        }
        "5" {
            $customConfig = Get-CustomConfig
            if (Start-Benchmark -Config $customConfig -ConfigName $customConfig.Name) {
                Generate-Report
                Show-LatestResults
            }
        }
        "0" {
            Write-Host ""
            Write-Host "Thank you for using! Goodbye!" -ForegroundColor Green
            Write-Host ""
            exit 0
        }
        default {
            Write-Host "[ERROR] Invalid option, please try again" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Read-Host "Press Enter to return to menu..."
    Clear-Host
    
} while ($true)
