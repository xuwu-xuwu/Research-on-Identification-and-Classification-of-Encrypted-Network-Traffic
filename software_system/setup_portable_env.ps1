param(
    [string]$Python = "python",
    [switch]$SkipPackageInstall
)

$ErrorActionPreference = "Stop"

$SoftwareDir = Resolve-Path -LiteralPath $PSScriptRoot
$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $SoftwareDir "..")
$VenvDir = Join-Path $SoftwareDir ".venv"
$Requirements = Join-Path $SoftwareDir "requirements.txt"
$EnvExample = Join-Path $SoftwareDir ".env.example"
$EnvFile = Join-Path $SoftwareDir ".env"

function Resolve-CandidatePath {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    $Expanded = [Environment]::ExpandEnvironmentVariables($Value)
    if ([System.IO.Path]::IsPathRooted($Expanded)) {
        if (Test-Path -LiteralPath $Expanded) {
            return (Resolve-Path -LiteralPath $Expanded).Path
        }
        return $null
    }

    foreach ($Base in @((Get-Location).Path, $ProjectRoot.Path, $SoftwareDir.Path)) {
        $Candidate = Join-Path $Base $Expanded
        if (Test-Path -LiteralPath $Candidate) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    return $null
}

function Find-Tshark {
    foreach ($EnvName in @("EIM_TSHARK_PATH", "TSHARK_PATH")) {
        $Value = [Environment]::GetEnvironmentVariable($EnvName)
        $Resolved = Resolve-CandidatePath $Value
        if ($Resolved) {
            return $Resolved
        }
    }

    foreach ($LocalValue in @("tools\tshark.exe", "tools\tshark", "bin\tshark.exe", "bin\tshark")) {
        $Resolved = Resolve-CandidatePath $LocalValue
        if ($Resolved) {
            return $Resolved
        }
    }

    $Command = Get-Command "tshark" -ErrorAction SilentlyContinue
    if ($Command -and $Command.Source) {
        return $Command.Source
    }

    foreach ($RegistryPath in @(
        "Registry::HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe",
        "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe",
        "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe"
    )) {
        try {
            $Key = Get-Item -LiteralPath $RegistryPath -ErrorAction Stop
            $Value = $Key.GetValue("")
            $Resolved = Resolve-CandidatePath $Value
            if ($Resolved) {
                return $Resolved
            }
        } catch {
            continue
        }
    }

    foreach ($EnvName in @("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432", "LocalAppData")) {
        $Base = [Environment]::GetEnvironmentVariable($EnvName)
        if ($Base) {
            $Resolved = Resolve-CandidatePath (Join-Path $Base "Wireshark\tshark.exe")
            if ($Resolved) {
                return $Resolved
            }
        }
    }

    return $null
}

function Set-EnvFileValue {
    param(
        [string]$Key,
        [string]$Value
    )

    if (-not (Test-Path -LiteralPath $EnvFile)) {
        if (Test-Path -LiteralPath $EnvExample) {
            Copy-Item -LiteralPath $EnvExample -Destination $EnvFile
        } else {
            New-Item -ItemType File -Path $EnvFile | Out-Null
        }
    }

    $Lines = Get-Content -LiteralPath $EnvFile -ErrorAction SilentlyContinue
    $Pattern = "^\s*$([regex]::Escape($Key))\s*="
    $Replacement = "$Key=$Value"
    $Updated = $false
    $NextLines = foreach ($Line in $Lines) {
        if ($Line -match $Pattern) {
            $Updated = $true
            $Replacement
        } else {
            $Line
        }
    }
    if (-not $Updated) {
        $NextLines += $Replacement
    }
    Set-Content -LiteralPath $EnvFile -Value $NextLines -Encoding UTF8
}

Write-Host "Software directory: $SoftwareDir"
Write-Host "Portable venv:      $VenvDir"

if (-not (Test-Path -LiteralPath (Join-Path $VenvDir "pyvenv.cfg"))) {
    Write-Host "Creating local Python environment..."
    & $Python -m venv $VenvDir
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VenvPython)) {
    $VenvPython = Join-Path $VenvDir "bin\python"
}
if (-not (Test-Path -LiteralPath $VenvPython)) {
    throw "Local Python executable was not found under $VenvDir."
}

if (-not $SkipPackageInstall) {
    Write-Host "Installing Python packages into software_system/.venv..."
    & $VenvPython -m pip install --upgrade pip
    & $VenvPython -m pip install -r $Requirements
}

$DetectedTshark = Find-Tshark
if ($DetectedTshark) {
    Set-EnvFileValue -Key "EIM_TSHARK_PATH" -Value $DetectedTshark
    Write-Host "Detected tshark:    $DetectedTshark"
} else {
    Set-EnvFileValue -Key "EIM_TSHARK_PATH" -Value "auto"
    Write-Host "Detected tshark:    not found"
    Write-Host "Put tshark.exe under software_system\tools\ or install Wireshark, then rerun this script."
}

Write-Host "Environment file:   $EnvFile"
Write-Host "Start backend with: .\software_system\start_backend.ps1"
