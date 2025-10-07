param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$wrapperProps = Join-Path $scriptDir 'gradle\wrapper\gradle-wrapper.properties'

if (-not (Test-Path -LiteralPath $wrapperProps)) {
    Write-Error "Gradle wrapper properties not found at $wrapperProps"
}

$distributionLine = Select-String -LiteralPath $wrapperProps -Pattern '^distributionUrl=' | Select-Object -First 1
if (-not $distributionLine) {
    Write-Error "distributionUrl missing from $wrapperProps"
}

$distributionUrl = $distributionLine.Line.Split('=', 2)[1] -replace '\\:', ':'
$distFileName = Split-Path $distributionUrl -Leaf

$gradleUserHome = if ($env:GRADLE_USER_HOME) { $env:GRADLE_USER_HOME } else { Join-Path $scriptDir '.gradle' }
$wrapperCacheDir = Join-Path $gradleUserHome 'wrapper\dists'
$archivePath = Join-Path $wrapperCacheDir $distFileName
$distDir = Join-Path $wrapperCacheDir ($distFileName -replace '\.zip$', '')

New-Item -ItemType Directory -Force -Path $wrapperCacheDir | Out-Null

if (-not (Test-Path -LiteralPath $archivePath)) {
    Write-Host "Downloading Gradle from $distributionUrl" -ForegroundColor Cyan
    try {
        Invoke-WebRequest -UseBasicParsing -Uri $distributionUrl -OutFile $archivePath
    } catch {
        if (Test-Path -LiteralPath $archivePath) { Remove-Item -LiteralPath $archivePath -Force }
        throw
    }
}

if (-not (Test-Path -LiteralPath $distDir)) {
    $tmpDir = "$distDir.tmp"
    if (Test-Path -LiteralPath $tmpDir) { Remove-Item -LiteralPath $tmpDir -Recurse -Force }
    New-Item -ItemType Directory -Path $tmpDir | Out-Null
    Write-Host "Extracting Gradle to $distDir" -ForegroundColor Cyan
    Expand-Archive -Path $archivePath -DestinationPath $tmpDir -Force
    $gradleFolder = Get-ChildItem -Path $tmpDir -Directory | Where-Object { $_.Name -like 'gradle-*' } | Select-Object -First 1
    if (-not $gradleFolder) {
        Remove-Item -LiteralPath $tmpDir -Recurse -Force
        throw "Could not find gradle directory inside archive"
    }
    Move-Item -Path $gradleFolder.FullName -Destination $distDir
    Remove-Item -LiteralPath $tmpDir -Recurse -Force
}

$gradleHome = Get-ChildItem -Path $distDir -Directory | Where-Object { $_.Name -like 'gradle-*' } | Select-Object -First 1
if (-not $gradleHome) {
    throw "Could not locate Gradle installation under $distDir"
}

$gradleExe = Join-Path $gradleHome.FullName 'bin\gradle.bat'
if (-not (Test-Path -LiteralPath $gradleExe)) {
    throw "Gradle executable not found at $gradleExe"
}

& $gradleExe '-p' $scriptDir @Args
exit $LASTEXITCODE
