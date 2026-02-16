#Requires -Version 5.0
# Test Menu Display - Shows what the menu looks like

Clear-Host

# Configuration variables
$Config1_Name = "Quick Test (3 minutes)"
$Config1_Description = "Fast verification during development"

$Config2_Name = "Standard Test (10 minutes) [RECOMMENDED]"
$Config2_Description = "Daily benchmark testing, most balanced"

$Config3_Name = "Long-term Test (30 minutes)"
$Config3_Description = "Observe long-term stability and memory leaks"

$Config4_Name = "Ultra-long Test (1 hour)"
$Config4_Description = "Extreme stress test, capacity planning"

$Config5_Name = "Custom Parameters"
$Config5_Description = "Customize test time and connection count"

# Display header
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PHP XAMPP NGINX Benchmark Tool" -ForegroundColor Cyan
Write-Host "   Interactive Configuration Menu" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Select Benchmark Mode:" -ForegroundColor Cyan
Write-Host ""

# Display menu items
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

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Menu display test completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
