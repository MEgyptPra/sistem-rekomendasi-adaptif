# debug_frontend_docker.ps1
# Usage: run from repository root (PowerShell)
#   .\pariwisata-recommender\frontend\scripts\debug_frontend_docker.ps1

$compose = "pariwisata-recommender\docker-compose.yml"
Write-Host "Using compose file: $compose"

# Get container ID for frontend service
$containerId = docker-compose -f $compose ps -q frontend 2>$null
if (-not $containerId) {
    Write-Host "No frontend container found (is it running?)."
    exit 1
}

Write-Host "Frontend container id: $containerId"

Write-Host "--- Container inspect ---"
docker inspect $containerId | Select-Object -First 1 | Out-Host

Write-Host "--- Last 200 lines of container logs ---"
docker logs --tail 200 $containerId | Out-Host

Write-Host "--- Container resource usage (single snapshot) ---"
docker stats --no-stream $containerId | Out-Host

Write-Host "--- Recent docker events for this container (may help find SIGTERM) ---"
docker events --filter container=$containerId --since (Get-Date).AddMinutes(-10) --until (Get-Date) --format '{{json .}}' | Out-Host

Write-Host "Done. Review logs above for errors, OOM, or signals."
