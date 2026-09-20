@echo off
setlocal
cd /d "%~dp0"
if /I "%~1"=="setup" (
  powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\bootstrap.ps1" %*
) else (
  powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run.ps1" %*
)
exit /b %errorlevel%
