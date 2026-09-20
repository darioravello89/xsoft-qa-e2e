#Requires -Version 5.1
# ExecutionPolicy Bypass is process-scoped in qa.cmd; no global policy is changed.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$OutputEncoding = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $OutputEncoding
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$qaCliArguments = $args
$qaRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $qaRoot

function Invoke-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo un requisito (codigo $LASTEXITCODE). Corregi el error anterior y repeti qa.cmd setup."
    }
}

function Find-Python312 {
    param([string]$RepositoryRoot = '')
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($RepositoryRoot) { $candidates.Add((Join-Path $RepositoryRoot '.venv\Scripts\python.exe')) }
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        # Windows PowerShell 5.1 may turn native stderr into a terminating error.
        # An installed launcher with no 3.12 runtime is a normal detection miss.
        try {
            $detected = & $launcher.Source -3.12 -c 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0 -and $detected) { $candidates.Add([string]$detected) }
        }
        catch { }
    }
    $candidates.Add((Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'))
    $candidates.Add((Join-Path $env:ProgramFiles 'Python312\python.exe'))
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            try {
                & $candidate -c 'import struct,sys; sys.exit(0 if sys.version_info[:2] == (3,12) and struct.calcsize(''P'') == 8 else 1)' 2>$null
                if ($LASTEXITCODE -eq 0) { return $candidate }
            }
            catch { }
        }
    }
    return $null
}

function Find-Java17 {
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($env:JAVA_HOME) { $candidates.Add($env:JAVA_HOME) }
    $javaCommand = Get-Command java.exe -ErrorAction SilentlyContinue
    if ($javaCommand) { $candidates.Add((Split-Path -Parent (Split-Path -Parent $javaCommand.Source))) }
    $adoptium = Join-Path $env:ProgramFiles 'Eclipse Adoptium'
    if (Test-Path -LiteralPath $adoptium) {
        Get-ChildItem -LiteralPath $adoptium -Directory -Filter 'jdk-17*' |
            Sort-Object Name -Descending | ForEach-Object { $candidates.Add($_.FullName) }
    }
    $javaVendor = Join-Path $env:ProgramFiles 'Java'
    if (Test-Path -LiteralPath $javaVendor) {
        Get-ChildItem -LiteralPath $javaVendor -Directory -Filter 'jdk-17*' |
            Sort-Object Name -Descending | ForEach-Object { $candidates.Add($_.FullName) }
    }
    foreach ($candidate in $candidates) {
        $release = Join-Path $candidate 'release'
        if (Test-Path -LiteralPath $release -PathType Leaf) {
            $metadata = Get-Content -LiteralPath $release -Raw
            if ($metadata -match 'JAVA_VERSION="17\.' -and $metadata -match 'OS_ARCH="(x86_64|amd64)"' -and
                (Test-Path -LiteralPath (Join-Path $candidate 'bin\java.exe')) -and
                (Test-Path -LiteralPath (Join-Path $candidate 'bin\jabswitch.exe')) -and
                (Test-Path -LiteralPath (Join-Path $candidate 'bin\WindowsAccessBridge-64.dll'))) {
                return $candidate
            }
        }
    }
    return $null
}

function Install-Requirement {
    param([string]$Id, [switch]$UserScope)
    $wingetCommand = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $wingetCommand) {
        throw 'Falta winget. Instala App Installer de Microsoft y repeti qa.cmd setup. https://aka.ms/getwinget'
    }
    Write-Host "Instalando $Id desde el catalogo oficial winget..."
    $installArgs = @('install', '--id', $Id, '--exact', '--source', 'winget', '--architecture', 'x64',
        '--accept-source-agreements', '--accept-package-agreements', '--silent', '--disable-interactivity')
    if ($UserScope) { $installArgs += @('--scope', 'user') }
    Invoke-Checked -Executable $wingetCommand.Source -Arguments $installArgs
}

try {
    if (-not [Environment]::Is64BitOperatingSystem) { throw 'Se necesita Windows de 64 bits.' }
    $qaPython = Find-Python312 -RepositoryRoot $qaRoot
    if (-not $qaPython) {
        Install-Requirement -Id 'Python.Python.3.12' -UserScope
        $qaPython = Find-Python312 -RepositoryRoot $qaRoot
        if (-not $qaPython) { throw 'Python 3.12 x64 no quedo disponible. Revisa la instalacion de winget.' }
    }
    $qaJava = Find-Java17
    if (-not $qaJava) {
        Install-Requirement -Id 'EclipseAdoptium.Temurin.17.JDK'
        $qaJava = Find-Java17
        if (-not $qaJava) { throw 'JDK 17 x64 con Java Access Bridge no quedo disponible.' }
    }
    $qaVenv = Join-Path $qaRoot '.venv'
    $qaVenvPython = Join-Path $qaVenv 'Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $qaVenv)) {
        Invoke-Checked -Executable $qaPython -Arguments @('-m', 'venv', $qaVenv)
    }
    if (-not (Test-Path -LiteralPath $qaVenvPython -PathType Leaf)) {
        throw '.venv existe pero esta incompleto. No se eliminara automaticamente; solicita ayuda al referente QA.'
    }
    Invoke-Checked -Executable $qaVenvPython -Arguments @('-c',
        'import struct,sys; sys.exit(0 if sys.version_info[:2] == (3,12) and struct.calcsize(''P'') == 8 else 1)')
    $qaHasPip = & $qaVenvPython -c 'import importlib.util; print(1 if importlib.util.find_spec(''pip'') else 0)'
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo verificar pip dentro de .venv.' }
    if ($qaHasPip -ne '1') {
        Invoke-Checked -Executable $qaVenvPython -Arguments @('-m', 'ensurepip', '--upgrade')
    }
    Invoke-Checked -Executable $qaVenvPython -Arguments @('-m', 'pip', 'install', '--disable-pip-version-check',
        '-r', (Join-Path $qaRoot 'requirements\windows.lock'))
    $env:JAVA_HOME = $qaJava
    $env:RC_JAVA_ACCESS_BRIDGE_DLL = Join-Path $qaJava 'bin\WindowsAccessBridge-64.dll'
    $env:PATH = (Join-Path $qaJava 'bin') + ';' + $env:PATH
    Invoke-Checked -Executable (Join-Path $qaJava 'bin\jabswitch.exe') -Arguments @('-enable')
    @{ java_home = $qaJava; python = $qaVenvPython } | ConvertTo-Json |
        Set-Content -LiteralPath (Join-Path $qaVenv 'qa-toolchain.json') -Encoding UTF8
    Write-Host 'Requisitos listos. Preparando el perfil local de QA...'
    if ($qaCliArguments.Count -eq 0) { $qaCliArguments = @('setup') }
    & $qaVenvPython -m framework.cli @qaCliArguments
    exit $LASTEXITCODE
}
catch {
    Write-Host "No se completo la instalacion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
