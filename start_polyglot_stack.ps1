# Polyglot Riff Atelier — One-Click Full-Stack Launcher (Docker Neo4j + pgvector + Seed + FastAPI + Browser)
param(
    [switch]$NoBrowser,
    [switch]$SkipEmbeddings
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "==> [1/4] Starting Neo4j 5 (+APOC) and PostgreSQL 17 (+pgvector:5433)..." -ForegroundColor Cyan

# Prefer active WSL2 Ubuntu Docker Engine if available, else Windows Docker CLI
$DriveLetter = $Root.Substring(0, 1).ToLower()
$RestOfPath = ($Root.Substring(2) -replace '\\', '/')
$WslComposePath = "/mnt/$DriveLetter$RestOfPath"
$WslDockerActive = $false
wsl -d Ubuntu -- bash -lc "docker info >/dev/null 2>&1" 2>$null
if ($LASTEXITCODE -eq 0) {
    $WslDockerActive = $true
    Write-Host "    Using active WSL2 Ubuntu Docker Engine..." -ForegroundColor Green
    # Keep WSL2 Ubuntu VM from auto-suspending after CLI exits
    $ExistingWslKeepalive = Get-CimInstance Win32_Process -Filter "Name = 'wsl.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'sleep infinity' }
    if (-not $ExistingWslKeepalive) {
        Start-Process -FilePath "wsl.exe" -ArgumentList "-d", "Ubuntu", "--", "sleep", "infinity" -WindowStyle Hidden
    }
    wsl -d Ubuntu -- docker compose -f "$WslComposePath/docker-compose.yml" up -d
} else {
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    Starting Windows Docker Desktop daemon..." -ForegroundColor Yellow
        docker desktop start *> $null
        for ($i = 0; $i -lt 30; $i++) {
            docker info *> $null
            if ($LASTEXITCODE -eq 0) { break }
            Start-Sleep -Seconds 3
        }
    }
    docker compose -f "$Root\docker-compose.yml" up -d
}

Write-Host "==> [2/4] Waiting for PostgreSQL (:5433) & Neo4j (:7687) readiness..." -ForegroundColor Cyan
$VenvPython = "$Root\.venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    python -m venv "$Root\.venv"
    & $VenvPython -m pip install -r "$Root\requirements.txt" -q
}

for ($i = 0; $i -lt 40; $i++) {
    $statusJson = & $VenvPython -m backend.cli status 2>$null
    if ($statusJson -and ($statusJson -match '"ok": true')) {
        break
    }
    Start-Sleep -Seconds 3
}

Write-Host "==> [3/4] Seeding 5-Language 2-Tier Corpus, bge-m3 Embeddings & Neo4j Graph..." -ForegroundColor Cyan
if ($SkipEmbeddings) {
    & $VenvPython -m backend.cli seed --no-embed
} else {
    & $VenvPython -m backend.cli seed
}

$PortListening = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if (-not $PortListening) {
    Write-Host "==> [4/4] Starting FastAPI Server + Suite Hub on http://0.0.0.0:8765 (LAN & Localhost)..." -ForegroundColor Green
    Start-Process -FilePath $VenvPython -ArgumentList "-m", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8765" -WorkingDirectory $Root -WindowStyle Hidden
    Start-Sleep -Seconds 2
} else {
    Write-Host "==> [4/4] FastAPI Server already active on port 8765" -ForegroundColor Green
}

$LanIp = (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' -and $_.PrefixOrigin -ne 'WellKnown' } | Select-Object -First 1).IPAddress
if ($LanIp) {
    Write-Host "    📱 Mobile / LAN Browser URL: http://$($LanIp):8765/index.html" -ForegroundColor Yellow
}

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:8765/index.html"
}
