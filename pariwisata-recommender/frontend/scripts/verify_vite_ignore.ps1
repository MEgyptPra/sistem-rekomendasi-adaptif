# verify_vite_ignore.ps1
# Usage: run from project root (PowerShell)
#   .\pariwisata-recommender\frontend\scripts\verify_vite_ignore.ps1

$frontendDir = Join-Path $PSScriptRoot ".."
$assetsDir = Join-Path $frontendDir "public\assets"
$testFile = Join-Path $assetsDir "vite-ignore-test.txt"

Write-Host "Touching test file: $testFile"
if (!(Test-Path $assetsDir)) {
    Write-Host "public/assets does not exist; creating for test"
    New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
}

# Write current timestamp into test file
Set-Content -Path $testFile -Value (Get-Date).ToString()
Write-Host "Wrote test file. Now tailing frontend logs (docker-compose). Press Ctrl+C to stop."

# Tail docker-compose logs for frontend service
"# Determine docker-compose file path (repo: parent of frontend)"
$composeFile = Join-Path (Split-Path -Parent $PSScriptRoot) "..\docker-compose.yml"
if (!(Test-Path $composeFile)) {
    Write-Host "Could not find docker-compose at: $composeFile" -ForegroundColor Yellow
    Write-Host "Try running docker-compose manually from repo root or adjust the script.";
} else {
    $resolved = Resolve-Path $composeFile
    Write-Host "Using docker-compose file: $resolved"

    # Use docker-compose to follow logs (this command will block)
    docker-compose -f "$resolved" logs -f frontend
}

# Note: On local dev (npm run dev) run `npm run dev` in the frontend folder and watch the terminal there instead of docker-compose logs.
