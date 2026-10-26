# PowerShell Launcher for Hangman Game
$ErrorActionPreference = "Stop"

$pythonCandidates = @(
    "$env:LOCALAPPDATA\Python\bin\python.exe",
    "py.exe",
    "python.exe"
)

$pyExe = $null
foreach ($cmd in $pythonCandidates) {
    if (Test-Path $cmd -PathType Leaf) {
        $pyExe = $cmd
        break
    }
    elseif (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pyExe = $cmd
        break
    }
}

if (-not $pyExe) {
    Write-Host "Error: Python executable not found." -ForegroundColor Red
    exit 1
}

$scriptPath = Join-Path $PSScriptRoot "hangman.py"
& $pyExe $scriptPath
