# Script pour démarrer ngrok dans une fenêtre visible et mettre à jour automatiquement les fichiers OpenAPI
# Usage: .\start-ngrok-and-update.ps1

Write-Host "🚀 Démarrage de ngrok et mise à jour automatique" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le backend tourne
Write-Host "1️⃣ Vérification du backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Backend en cours d'exécution" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend non accessible. Lancez-le d'abord:" -ForegroundColor Yellow
    Write-Host "      cd backend && py -m uvicorn main:app --port 3001" -ForegroundColor Cyan
    exit 1
}

# Démarrer ngrok dans une nouvelle fenêtre
Write-Host "`n2️⃣ Démarrage de ngrok dans une nouvelle fenêtre..." -ForegroundColor Yellow
$ngrokCommand = "Write-Host 'Ngrok demarre!' -ForegroundColor Green; Write-Host ''; Write-Host 'Attendez que l URL s affiche ci-dessous...' -ForegroundColor Yellow; Write-Host ''; ngrok http 3001"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $ngrokCommand

Write-Host "   ✅ Fenêtre ngrok ouverte" -ForegroundColor Green
Write-Host "   👀 Regardez la fenêtre ngrok pour voir l'URL (ex: https://abc123.ngrok-free.app)" -ForegroundColor Cyan

# Attendre et récupérer l'URL
Write-Host "`n3️⃣ Attente de l'URL ngrok..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

$maxRetries = 15
$retry = 0
$ngrokUrl = $null

while ($retry -lt $maxRetries -and -not $ngrokUrl) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
        if ($response.tunnels.Count -gt 0) {
            $ngrokUrl = $response.tunnels[0].public_url
            Write-Host "   ✅ URL détectée: $ngrokUrl" -ForegroundColor Green
            break
        }
    } catch {
        $retry++
        if ($retry -lt $maxRetries) {
            Write-Host "   ⏳ Tentative $retry/$maxRetries..." -ForegroundColor Gray
            Start-Sleep -Seconds 2
        }
    }
}

if (-not $ngrokUrl) {
    Write-Host "   ⚠️  Impossible de détecter automatiquement l'URL" -ForegroundColor Yellow
    Write-Host "   💡 Copiez l'URL depuis la fenêtre ngrok (ex: https://abc123.ngrok-free.app)" -ForegroundColor Cyan
    $manualUrl = Read-Host "   Entrez l'URL ngrok manuellement"
    if ($manualUrl) {
        $ngrokUrl = $manualUrl
        Write-Host "   ✅ URL manuelle: $ngrokUrl" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Aucune URL fournie. Arrêt." -ForegroundColor Red
        exit 1
    }
}

# Mettre à jour les fichiers OpenAPI
Write-Host "`n4️⃣ Mise à jour des fichiers OpenAPI..." -ForegroundColor Yellow

$files = @(
    "appPackage/apiSpecificationFile/openapi.yaml",
    "appPackage/apiSpecificationFile/openapi_1.yaml",
    "appPackage/apiSpecificationFile/openapi_2.yaml",
    "appPackage/apiSpecificationFile/openapi_3.yaml"
)

$updatedCount = 0
foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $newContent = $content -replace 'http://localhost:3001', $ngrokUrl
        
        if ($content -ne $newContent) {
            Set-Content -Path $file -Value $newContent -NoNewline
            Write-Host "   ✅ $file" -ForegroundColor Green
            $updatedCount++
        } else {
            Write-Host "   ⏭️  $file (déjà à jour)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  $file (introuvable)" -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Configuration terminée!" -ForegroundColor Green
Write-Host "   📦 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Dans Teams Toolkit, cliquez sur 'Provision' ou 'Deploy' pour rebuilder le ZIP" -ForegroundColor White
Write-Host "   2. Ouvrez Teams Desktop" -ForegroundColor White
Write-Host "   3. Apps → Manage your apps → Upload a custom app" -ForegroundColor White
Write-Host "   4. Sélectionnez: appPackage/build/appPackage.dev.zip" -ForegroundColor White
Write-Host ""
Write-Host "   IMPORTANT: Gardez ngrok ET le backend en cours d execution pendant vos tests!" -ForegroundColor Yellow
Write-Host "   📋 URL ngrok utilisée: $ngrokUrl" -ForegroundColor Gray

