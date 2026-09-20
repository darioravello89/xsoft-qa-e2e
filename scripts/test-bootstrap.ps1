#Requires -Version 5.1
# Read-only check: parse scripts and run only prerequisite detection functions.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
foreach ($qaFile in @('bootstrap.ps1', 'run.ps1', 'test-bootstrap.ps1')) {
    $qaTokens = $null
    $qaErrors = $null
    $qaAst = [System.Management.Automation.Language.Parser]::ParseFile(
        (Join-Path $PSScriptRoot $qaFile), [ref]$qaTokens, [ref]$qaErrors)
    if ($qaErrors.Count) { throw "Error de sintaxis en $qaFile : $qaErrors" }
    if ($qaFile -eq 'bootstrap.ps1') { $qaBootstrapAst = $qaAst }
}
$qaFunctions = $qaBootstrapAst.FindAll({
    param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst]
}, $false)
. ([scriptblock]::Create(($qaFunctions | ForEach-Object { $_.Extent.Text }) -join "`n"))
$qaDetectedPython = Find-Python312
$qaDetectedJava = Find-Java17
Write-Host "PowerShell $($PSVersionTable.PSVersion): sintaxis valida; deteccion sin instalar."
Write-Host "Python 3.12 x64 disponible: $([bool]$qaDetectedPython)"
Write-Host "JDK 17 x64 disponible: $([bool]$qaDetectedJava)"
