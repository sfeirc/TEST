# Script pour tester que votre backend déployé fonctionne
# Usage: .\test-backend-url.ps1 -Url "https://your-backend-url.com"

param(
    [Parameter(Mandatory=$true)]
    [string]$Url
)

Write-Host "🧪 Test du backend à l'URL: $Url" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health check
Write-Host "1️⃣ Test Health Check..." -ForegroundColor Yellow
try {
    $healthUrl = "$Url/health"
    $response = Invoke-WebRequest -Uri $healthUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Health check OK" -ForegroundColor Green
        Write-Host "   Réponse: $($response.Content)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Health check échoué: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Root endpoint
Write-Host "`n2️⃣ Test Root Endpoint..." -ForegroundColor Yellow
try {
    $rootUrl = "$Url/"
    $response = Invoke-WebRequest -Uri $rootUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Root endpoint OK" -ForegroundColor Green
        $json = $response.Content | ConvertFrom-Json
        Write-Host "   Message: $($json.message)" -ForegroundColor Gray
        Write-Host "   Version: $($json.version)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Root endpoint échoué: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: CORS headers (si accessible)
Write-Host "`n3️⃣ Test CORS Configuration..." -ForegroundColor Yellow
try {
    $optionsUrl = "$Url/"
    $response = Invoke-WebRequest -Uri $optionsUrl -Method OPTIONS -TimeoutSec 10 -ErrorAction Stop
    Write-Host "   ✅ OPTIONS request acceptée" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  OPTIONS request non supportée (peut être normal)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✨ Tests terminés!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Si tous les tests passent, votre backend est prêt!" -ForegroundColor White
Write-Host "   2. Mettez à jour les fichiers OpenAPI:" -ForegroundColor White
Write-Host "      .\update-openapi-url.ps1 -NewUrl `"$Url`"" -ForegroundColor Cyan
Write-Host "   3. Rebuild le package Teams et upload dans Teams" -ForegroundColor White

