param(
    [string]$HostName = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

$VenvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VenvPython)) {
    $VenvPython = Join-Path $PSScriptRoot ".venv\bin\python"
}
if (-not (Test-Path -LiteralPath $VenvPython)) {
    throw "Portable dependencies are not installed. Run .\software_system\setup_portable_env.ps1 first."
}

& $VenvPython -m uvicorn software_system.backend.app.main:app --host $HostName --port $Port
