# Railway Deployment Script
# Run this after: railway login

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Railway Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if logged in
Write-Host "Checking Railway authentication..." -ForegroundColor Yellow
railway whoami
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Not logged in. Please run: railway login" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Initializing Railway project (if not already linked)..." -ForegroundColor Yellow
railway init

Write-Host ""
Write-Host "Linking to existing project (if needed)..." -ForegroundColor Yellow
railway link

Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
Write-Host "Note: Make sure to set these in Railway dashboard:" -ForegroundColor Yellow
Write-Host "  - AZURE_OPENAI_ENDPOINT" -ForegroundColor Yellow
Write-Host "  - AZURE_OPENAI_KEY" -ForegroundColor Yellow
Write-Host "  - AZURE_OPENAI_DEPLOYMENT" -ForegroundColor Yellow
Write-Host "  - PORT (auto-set by Railway)" -ForegroundColor Yellow
Write-Host ""

Write-Host "Deploying to Railway..." -ForegroundColor Green
railway up

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment initiated!" -ForegroundColor Green
Write-Host "Check progress at: https://railway.app" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

