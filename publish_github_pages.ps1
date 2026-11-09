# Polyglot Riff Studio — 1-Click GitHub Pages Publisher & Shard Exporter
param(
    [string]$CommitMessage = "Update Polyglot Riff Studio & db/*.db.json shards"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$VenvPython = "$Root\.venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    Write-Host "==> [1/3] Exporting deterministic db/*.db.json shards..." -ForegroundColor Cyan
    & $VenvPython -m backend.cli export-shards
}

Write-Host "==> [2/3] Staging & committing changes..." -ForegroundColor Cyan
git add -A
$status = git status --porcelain
if ($status) {
    git commit -m $CommitMessage
} else {
    Write-Host "    Working tree clean (no new changes to commit)." -ForegroundColor Yellow
}

Write-Host "==> [3/3] Pushing to GitHub (main)..." -ForegroundColor Green
git push -u origin main
Write-Host "✓ Published! GitHub Pages URL: https://hotpopize.github.io/polyglot-riff-studio/" -ForegroundColor Green
