#Requires -Version 5.0
# PHP XAMPP NGINX Benchmark - Interactive Menu Configuration

Clear-Host

# Configuration presets
$Config1_Name = "Quick Regression (3 minutes)"
$Config1_Duration = 180
$Config1_Connections = 100
$Config1_Description = "Daily development check (recommended 50~100)"

$Config2_Name = "Pre-commit Comparison (10 minutes)"
$Config2_Duration = 600
$Config2_Connections = 300
$Config2_Description = "Version comparison before commit (recommended 200~300)"

$Config3_Name = "Bottleneck Locator (15 minutes x 3 rounds)"
$Config3_Duration = 900
$Config3_Connections_R1 = 300
$Config3_Connections_R2 = 600
$Config3_Connections_R3 = 1000
$Config3_Description = "Run three independent rounds: 300 -> 600 -> 1000"

$Config4_Name = "Pre-production Validation (30 minutes)"
$Config4_Duration = 1800
$Config4_Connections = 800
$Config4_Description = "Release gate test (recommended 500~800)"

$Config5_Name = "Soak Test (8 hours)"
$Config5_Duration = 28800
$Config5_Connections = 700
$Config5_Description = "Long stability run (recommended 300~700)"

$Config6_Name = "Extreme Endurance (8 hours)"
$Config6_Duration = 28800
$Config6_Connections = 1000
$Config6_Description = "Low-frequency limit drill (weekly/monthly)"

$Config7_Name = "Custom Parameters"
$Config7_Description = "Customize test time and connection count"

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

    Write-Host "  6. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config6_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config6_Description -ForegroundColor Gray
    Write-Host ""

    Write-Host "  7. " -ForegroundColor Yellow -NoNewline
    Write-Host $Config7_Name -ForegroundColor White
    Write-Host "     -> " -ForegroundColor Yellow -NoNewline
    Write-Host $Config7_Description -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "  0. " -ForegroundColor Magenta -NoNewline
    Write-Host "Exit" -ForegroundColor Magenta
    Write-Host ""
}

function Format-DurationDisplay {
    param(
        [int]$Seconds
    )

    $safeSeconds = [math]::Max(0, [int]$Seconds)

    if ($safeSeconds -lt 60) {
        return "${safeSeconds}s"
    }

    if ($safeSeconds -le 1800) {
        $minutes = [int][math]::Floor($safeSeconds / 60)
        $remainingSeconds = $safeSeconds % 60
        if ($remainingSeconds -eq 0) {
            return "${minutes}m"
        }
        return "${minutes}m ${remainingSeconds}s"
    }

    $hours = [int][math]::Floor($safeSeconds / 3600)
    $remainingMinutes = [int][math]::Floor(($safeSeconds % 3600) / 60)
    if ($remainingMinutes -eq 0) {
        return "${hours}h"
    }
    return "${hours}h ${remainingMinutes}m"
}


function Get-CustomConfig {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Custom Configuration" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $endpointInputs = @(
        @{ Name = "cpu.php"; Label = "CPU endpoint" },
        @{ Name = "json.php"; Label = "JSON endpoint" },
        @{ Name = "io.php"; Label = "I/O endpoint" }
    )

    $endpointPlan = @{}

    foreach ($endpoint in $endpointInputs) {
        Write-Host ""
        Write-Host "  [$($endpoint.Label)]" -ForegroundColor Yellow

        do {
            Write-Host "    Enter duration in seconds (min: 10): " -ForegroundColor Cyan -NoNewline
            $duration = Read-Host
            if ($duration -notmatch '^\d+$' -or [int]$duration -lt 10) {
                Write-Host "[ERROR] Please enter a number greater than or equal to 10" -ForegroundColor Red
                continue
            }
            break
        } while ($true)

        do {
            Write-Host "    Enter concurrent connections (min: 1): " -ForegroundColor Cyan -NoNewline
            $connections = Read-Host
            if ($connections -notmatch '^\d+$' -or [int]$connections -lt 1) {
                Write-Host "[ERROR] Please enter a number greater than 0" -ForegroundColor Red
                continue
            }
            break
        } while ($true)

        $endpointPlan[$endpoint.Name] = @{
            Duration = [int]$duration
            Connections = [int]$connections
        }
    }
    
    return @{
        Name        = "Custom Configuration"
        Duration    = 0
        Connections = 0
        EndpointPlan = $endpointPlan
    }
}

function Get-EndpointPlan {
    param(
        [hashtable]$Config,
        [ValidateSet("sequential", "parallel")]
        [string]$EndpointSchedule,
        [int]$EndpointCount
    )

    if ($Config.ContainsKey("EndpointPlan") -and $Config.EndpointPlan) {
        return $Config.EndpointPlan
    }

    if ($EndpointSchedule -eq "parallel") {
        $perEndpointDuration = [math]::Max(1, [int]$Config.Duration)
    }
    else {
        $perEndpointDuration = [math]::Max(1, [int][math]::Ceiling($Config.Duration / [double][math]::Max(1, $EndpointCount)))
    }

    return @{
        "cpu.php" = @{ Duration = $perEndpointDuration; Connections = [int]$Config.Connections }
        "json.php" = @{ Duration = $perEndpointDuration; Connections = [int]$Config.Connections }
        "io.php" = @{ Duration = $perEndpointDuration; Connections = [int]$Config.Connections }
    }
}

function Get-EndpointSchedule {
    Write-Host ""
    Write-Host "Select Endpoint Execution Schedule:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. " -ForegroundColor Yellow -NoNewline
    Write-Host "Sequential (Isolated)" -ForegroundColor White
    Write-Host "     -> Split total duration across cpu/json/io, run endpoints one by one" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. " -ForegroundColor Yellow -NoNewline
    Write-Host "Parallel (Mixed Load)" -ForegroundColor White
    Write-Host "     -> Each endpoint runs full duration at the same time (higher combined load)" -ForegroundColor Gray
    Write-Host ""

    do {
        $modeChoice = Read-Host "Select schedule (1-2)"
        switch ($modeChoice) {
            "1" {
                return @{
                    Mode = "sequential"
                    Name = "Sequential (Isolated)"
                }
            }
            "2" {
                return @{
                    Mode = "parallel"
                    Name = "Parallel (Mixed Load)"
                }
            }
            default {
                Write-Host "[ERROR] Invalid option, please choose 1 or 2" -ForegroundColor Red
            }
        }
    } while ($true)
}


function Show-ConfigSummary {
    param(
        [hashtable]$Config,
        [string]$ConfigName,
        [int]$EndpointCount,
        [ValidateSet("sequential", "parallel")]
        [string]$EndpointSchedule = "sequential",
        [hashtable]$EndpointPlan
    )

    $endpointNames = @("cpu.php", "json.php", "io.php")
    if (-not $EndpointPlan) {
        $EndpointPlan = Get-EndpointPlan -Config $Config -EndpointSchedule $EndpointSchedule -EndpointCount $EndpointCount
    }

    $durations = @()
    $connectionsList = @()
    foreach ($ep in $endpointNames) {
        $durations += [int]$EndpointPlan[$ep].Duration
        $connectionsList += [int]$EndpointPlan[$ep].Connections
    }

    if ($EndpointSchedule -eq "parallel") {
        $effectiveTotalDuration = ($durations | Measure-Object -Maximum).Maximum
        $scheduleName = "Parallel (Mixed Load)"
    }
    else {
        $effectiveTotalDuration = ($durations | Measure-Object -Sum).Sum
        $scheduleName = "Sequential (Isolated)"
    }

    $uniqueDurations = @($durations | Select-Object -Unique)
    $uniqueConnections = @($connectionsList | Select-Object -Unique)
    $maxConnections = [int](($connectionsList | Measure-Object -Maximum).Maximum)
    $sumConnections = [int](($connectionsList | Measure-Object -Sum).Sum)

    if ($uniqueDurations.Count -eq 1) {
        $perEndpointDurationText = Format-DurationDisplay -Seconds ([int]$uniqueDurations[0])
    } else {
        $perEndpointDurationText = "varies by endpoint"
    }

    if ($uniqueConnections.Count -eq 1) {
        $connectionsText = "$($uniqueConnections[0])"
    } else {
        $connectionsText = "varies by endpoint"
    }

    if ($EndpointSchedule -eq "parallel") {
        $peakClientConcurrency = $sumConnections * 2
        $loadHint = "All endpoint stages run together. Client workers add up across endpoints."
    } else {
        $peakClientConcurrency = $maxConnections * 2
        $loadHint = "Endpoint stages run one by one. Only one endpoint stage is active at a time."
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Configuration Summary" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Selected Mode: " -ForegroundColor White -NoNewline
    Write-Host "$ConfigName" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Parameters:" -ForegroundColor White
    Write-Host "    * Endpoint Schedule: $scheduleName" -ForegroundColor White
    Write-Host "    * Total Duration: $(Format-DurationDisplay -Seconds $effectiveTotalDuration)" -ForegroundColor White
    Write-Host "    * Per Endpoint Duration: $perEndpointDurationText" -ForegroundColor Gray
    Write-Host "    * Connections: $connectionsText" -ForegroundColor White
    Write-Host "    * Peak Client Concurrency (XAMPP + NGINX-Multi): $peakClientConcurrency" -ForegroundColor White
    Write-Host "    * Load Hint: $loadHint" -ForegroundColor DarkYellow
    Write-Host "    * Endpoint Stage Plan:" -ForegroundColor Gray
    foreach ($ep in $endpointNames) {
        $runType = if ($EndpointSchedule -eq "parallel") { "parallel" } else { "sequential" }
        Write-Host "      - ${ep}: Duration $(Format-DurationDisplay -Seconds ([int]$EndpointPlan[$ep].Duration)), Connections $([int]$EndpointPlan[$ep].Connections) ($runType)" -ForegroundColor Gray
    }
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
        "  Progress: $bar $percentage% | Elapsed: $(Format-DurationDisplay -Seconds $ElapsedSeconds) | Remaining: $(Format-DurationDisplay -Seconds $remaining)"
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
        [string]$ConfigName,
        [switch]$SkipConfirm,
        [ValidateSet("sequential", "parallel")]
        [string]$EndpointSchedule = "sequential"
    )

    if (-not (Test-DockerReadiness)) {
        return $false
    }

    $endpointCount = 3
    $endpointPlan = Get-EndpointPlan -Config $Config -EndpointSchedule $EndpointSchedule -EndpointCount $endpointCount

    $cpuDuration = [int]$endpointPlan["cpu.php"].Duration
    $jsonDuration = [int]$endpointPlan["json.php"].Duration
    $ioDuration = [int]$endpointPlan["io.php"].Duration

    $cpuConnections = [int]$endpointPlan["cpu.php"].Connections
    $jsonConnections = [int]$endpointPlan["json.php"].Connections
    $ioConnections = [int]$endpointPlan["io.php"].Connections

    if ($EndpointSchedule -eq "parallel") {
        $effectiveTotalDuration = [int]([math]::Max($cpuDuration, [math]::Max($jsonDuration, $ioDuration)))
    }
    else {
        $effectiveTotalDuration = $cpuDuration + $jsonDuration + $ioDuration
    }

    $perEndpointDuration = [int][math]::Ceiling(($cpuDuration + $jsonDuration + $ioDuration) / 3)
    
    Show-ConfigSummary -Config $Config -ConfigName $ConfigName -EndpointCount $endpointCount -EndpointSchedule $EndpointSchedule -EndpointPlan $endpointPlan
    
    if (-not $SkipConfirm) {
        Write-Host "Confirm to start? (Y/N) [Press Enter for Yes]: " -ForegroundColor Cyan -NoNewline
        $confirm = Read-Host
    }
    else {
        $confirm = "Y"
    }

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
    try {
        # Create temp file for benchmark output
        $outputFile = "$env:TEMP\benchmark_$([guid]::NewGuid()).txt"
        
        # Start benchmark in background and capture process output to file
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "cmd.exe"
        # Use array for arguments to properly handle quotes and spaces
        $composeArgs = @(
            "run", "--rm",
            "-e", "DURATION=$perEndpointDuration",
            "-e", "PER_ENDPOINT_DURATION=$perEndpointDuration",
            "-e", "TOTAL_DURATION=$effectiveTotalDuration",
            "-e", "CONNECTIONS=$cpuConnections",
            "-e", "CPU_DURATION=$cpuDuration",
            "-e", "JSON_DURATION=$jsonDuration",
            "-e", "IO_DURATION=$ioDuration",
            "-e", "CPU_CONNECTIONS=$cpuConnections",
            "-e", "JSON_CONNECTIONS=$jsonConnections",
            "-e", "IO_CONNECTIONS=$ioConnections",
            "-e", "ENDPOINT_SCHEDULE=$EndpointSchedule",
            "benchmark"
        )
        $composeCommand = "docker-compose " + ([System.String]::Join(" ", $composeArgs)) + " > `"$outputFile`" 2>&1"
        $processInfo.Arguments = "/c $composeCommand"
        $processInfo.UseShellExecute = $false
        # Output is redirected by cmd, so no stream redirection needed here.
        $processInfo.RedirectStandardOutput = $false
        $processInfo.RedirectStandardError = $false
        $processInfo.CreateNoWindow = $true
        
        $process = [System.Diagnostics.Process]::Start($processInfo)
        
        # Progress bar with countdown (shared logic for all menu options).
        # Sequential mode: endpoints split total duration and run one by one.
        # Parallel mode: each endpoint runs for full duration concurrently.
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
            Write-Host "   Elapsed: $(Format-DurationDisplay -Seconds ([int][math]::Round($elapsed.TotalSeconds))) (estimated around $(Format-DurationDisplay -Seconds $estimatedTotalSeconds))" -ForegroundColor Red
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
            Write-Host "   Elapsed: $(Format-DurationDisplay -Seconds ([int][math]::Round($elapsed.TotalSeconds))) (estimated around $(Format-DurationDisplay -Seconds $estimatedTotalSeconds))" -ForegroundColor Yellow
            Write-Host "   This is not a failure." -ForegroundColor Green
            Write-Host "   Possible reason: ApacheBench reached request limits before timeout." -ForegroundColor DarkYellow
            Write-Host ""
        }
        
        Write-Host ""
        Write-Host ""
        Write-Host "[SUCCESS] Benchmark completed!" -ForegroundColor Green
        Write-Host "   Total Duration: $(Format-DurationDisplay -Seconds ([int][math]::Round($elapsed.TotalSeconds)))" -ForegroundColor Green
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
        $reportOutput = python tools/generate_report.py 2>&1
        $pythonExitCode = $LASTEXITCODE
        if ($reportOutput) {
            $reportOutput | ForEach-Object { Write-Host $_ }
        }
        if ($pythonExitCode -ne 0) {
            throw "Report generation failed with exit code $pythonExitCode"
        }

        $generatedReportPath = $null
        foreach ($line in $reportOutput) {
            if ($line -match '^Report generated:\s*(.+)$') {
                $generatedReportPath = $Matches[1].Trim()
            }
        }

        if (-not $generatedReportPath) {
            $latestReport = Get-ChildItem reports/ -File -Filter "report_*.html" -ErrorAction SilentlyContinue |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1
            if ($latestReport) {
                $generatedReportPath = $latestReport.FullName
            }
            else {
                $generatedReportPath = "reports/report.html"
            }
        }

        Write-Host ""
        Write-Host "[SUCCESS] Report generated!" -ForegroundColor Green
        Write-Host "   Location: $generatedReportPath" -ForegroundColor Green
        Write-Host ""

        Start-Process $generatedReportPath
        Write-Host "[INFO] Opening report in browser..." -ForegroundColor Green
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

    $choicePrompt = "Select option (1-7, 0 to exit) [Press Enter for 2]: "
    $choice = Read-Host $choicePrompt
    if ([string]::IsNullOrWhiteSpace($choice)) {
        $choice = "2"  # 預設選擇 2
    }
    if ($choice -eq "0") {
        Write-Host ""
        Write-Host "Thank you for using! Goodbye!" -ForegroundColor Green
        Write-Host ""
        exit 0
    }

    if ($choice -notin @("1", "2", "3", "4", "5", "6", "7")) {
        Write-Host "[ERROR] Invalid option, please try again" -ForegroundColor Red
        exit 1
    }

    # 還原互動式 Endpoint Schedule 選單與提示
    Write-Host ""
    Write-Host "Select Endpoint Execution Schedule:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. " -ForegroundColor Yellow -NoNewline
    Write-Host "Sequential (Isolated)" -ForegroundColor White
    Write-Host "     -> Split total duration across cpu/json/io, run endpoints one by one" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. " -ForegroundColor Yellow -NoNewline
    Write-Host "Parallel (Mixed Load)" -ForegroundColor White
    Write-Host "     -> Each endpoint runs full duration at the same time (higher combined load)" -ForegroundColor Gray
    Write-Host ""
    $schedulePrompt = "Select schedule (1-2) [Press Enter for 1]: "
    $selectedScheduleInput = Read-Host $schedulePrompt
    if ([string]::IsNullOrWhiteSpace($selectedScheduleInput)) {
        $selectedScheduleInput = "1"  # 預設選擇 1
    }
    switch ($selectedScheduleInput) {
        "1" {
            $selectedSchedule = @{ Mode = "sequential"; Name = "Sequential (Isolated)" }
        }
        "2" {
            $selectedSchedule = @{ Mode = "parallel"; Name = "Parallel (Mixed Load)" }
        }
        default {
            Write-Host "[ERROR] Invalid schedule option, please choose 1 or 2" -ForegroundColor Red
            exit 1
        }
    }
    
    switch ($choice) {
        "1" {
            if (Start-Benchmark -Config @{Duration = $Config1_Duration; Connections = $Config1_Connections} -ConfigName $Config1_Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "2" {
            if (Start-Benchmark -Config @{Duration = $Config2_Duration; Connections = $Config2_Connections} -ConfigName $Config2_Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "3" {
            $stressConnections = @($Config3_Connections_R1, $Config3_Connections_R2, $Config3_Connections_R3)
            $roundIndex = 0
            $allRoundsPassed = $true

            foreach ($roundConnections in $stressConnections) {
                $roundIndex++
                $roundName = "$Config3_Name (Round ${roundIndex}/$($stressConnections.Count), ${roundConnections} connections)"
                $roundSkipConfirm = $roundIndex -gt 1

                $roundOk = Start-Benchmark -Config @{Duration = $Config3_Duration; Connections = $roundConnections} -ConfigName $roundName -SkipConfirm:$roundSkipConfirm -EndpointSchedule $selectedSchedule.Mode
                if (-not $roundOk) {
                    $allRoundsPassed = $false
                    break
                }
            }

            if ($allRoundsPassed) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "4" {
            if (Start-Benchmark -Config @{Duration = $Config4_Duration; Connections = $Config4_Connections} -ConfigName $Config4_Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "5" {
            if (Start-Benchmark -Config @{Duration = $Config5_Duration; Connections = $Config5_Connections} -ConfigName $Config5_Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "6" {
            if (Start-Benchmark -Config @{Duration = $Config6_Duration; Connections = $Config6_Connections} -ConfigName $Config6_Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
        "7" {
            $customConfig = Get-CustomConfig
            if (Start-Benchmark -Config $customConfig -ConfigName $customConfig.Name -EndpointSchedule $selectedSchedule.Mode) {
                Generate-Report
                Show-LatestResults
                exit 0
            }
            exit 1
        }
    }

    exit 1
    
} while ($true)
