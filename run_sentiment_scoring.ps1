# Background sentiment intensity scoring runner
# Runs the sentiment_intensity_score.py script with error handling and logging

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $projectRoot "analysis/scripts/sentiment_intensity_score.py"
$logFile = Join-Path $projectRoot "logs/sentiment_intensity_background.log"

# Create logs directory if needed
$logsDir = Join-Path $projectRoot "logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$message = "$timestamp - Starting sentiment intensity scoring..."
Add-Content -Path $logFile -Value $message
Write-Host $message

try {
    Set-Location $projectRoot
    $output = python $scriptPath 2>&1
    Add-Content -Path $logFile -Value ($output | Out-String)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "$timestamp - Completed"
} catch {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $error = "$timestamp - Error: $_"
    Add-Content -Path $logFile -Value $error
    Write-Error $error
}
