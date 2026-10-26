@echo off
title Hangman Game - CodeAlpha Task 1
chcp 65001 >nul 2>&1

:: Attempt to locate the functional Python executable
set "PY_CMD="

:: Check direct Python installation path
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set "PY_CMD=%LOCALAPPDATA%\Python\bin\python.exe"
    goto :RUN
)

:: Check py launcher
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=py"
    goto :RUN
)

:: Check python in PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
    goto :RUN
)

echo [ERROR] Python was not found on your system.
echo Please install Python from https://www.python.org/downloads/
pause
exit /b 1

:RUN
"%PY_CMD%" "%~dp0hangman.py"
pause
