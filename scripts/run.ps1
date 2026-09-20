#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$OutputEncoding = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $OutputEncoding
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$qaCliArguments = $args
$qaRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $qaRoot
try {
    $qaPython = Join-Path $qaRoot '.venv\Scripts\python.exe'
    $qaTools = Join-Path $qaRoot '.venv\qa-toolchain.json'
    if (-not (Test-Path -LiteralPath $qaPython -PathType Leaf) -or
        -not (Test-Path -LiteralPath $qaTools -PathType Leaf)) {
        throw 'Primero ejecuta qa.cmd setup. Este comando no instala ni actualiza requisitos.'
    }
    $qaToolchain = Get-Content -LiteralPath $qaTools -Raw | ConvertFrom-Json
    $qaJava = [string]$qaToolchain.java_home
    if (-not (Test-Path -LiteralPath (Join-Path $qaJava 'bin\java.exe') -PathType Leaf)) {
        throw 'El JDK configurado ya no existe. Repeti qa.cmd setup.'
    }
    $env:JAVA_HOME = $qaJava
    $env:RC_JAVA_ACCESS_BRIDGE_DLL = Join-Path $qaJava 'bin\WindowsAccessBridge-64.dll'
    $env:PATH = (Join-Path $qaJava 'bin') + ';' + $env:PATH
    & $qaPython -m framework.cli @qaCliArguments
    exit $LASTEXITCODE
}
catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
