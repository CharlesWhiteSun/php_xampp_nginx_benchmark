@echo off
REM PHP XAMPP NGINX Benchmark - Interactive Menu Launcher

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: PowerShell not found
    echo Please ensure PowerShell 5.0 or higher is installed
    echo.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker Compose not found
    echo Please ensure Docker Desktop is installed and running
    echo.
    pause
    exit /b 1
)

REM Run the PowerShell script
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%~dp0start_benchmark.ps1'"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Script execution failed. Please check your configuration.
    echo.
    pause
)

