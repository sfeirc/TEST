# Script pour démarrer le backend ET ngrok en même temps
# Usage: .\start-backend-and-ngrok.ps1

Write-Host "🚀 Démarrage du backend et ngrok" -ForegroundColor Cyan
Write-Host ""

# Vérifier que ngrok est installé
Write-Host "1️⃣ Vérification de ngrok..." -ForegroundColor Yellow
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "   ✅ ngrok installé" -ForegroundColor Green
} catch {
    Write-Host "   ❌ ngrok non trouvé. Installez-le d'abord:" -ForegroundColor Red
    Write-Host "      .\setup-ngrok.ps1" -ForegroundColor Cyan
    exit 1
}

# Démarrer le backend dans une nouvelle fenêtre
Write-Host "`n2️⃣ Démarrage du backend dans une nouvelle fenêtre..." -ForegroundColor Yellow
$backendPath = Resolve-Path "backend"
$backendCommand = "cd '$backendPath'; Write-Host '🚀 Démarrage du backend FastAPI...' -ForegroundColor Green; Write-Host 'Port: 3001' -ForegroundColor Cyan; Write-Host ''; py -m uvicorn main:app --port 3001 --host 0.0.0.0; Write-Host ''; Write-Host 'Backend arrêté. Appuyez sur une touche pour fermer...' -ForegroundColor Yellow; Read-Host"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand

Write-Host "   ✅ Fenêtre backend ouverte" -ForegroundColor Green
Write-Host "   ⏳ Attente du démarrage du backend (10 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Vérifier que le backend répond
Write-Host "`n3️⃣ Vérification du backend..." -ForegroundColor Yellow
$maxRetries = 5
$retry = 0
$backendReady = $false

while ($retry -lt $maxRetries -and -not $backendReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Backend opérationnel!" -ForegroundColor Green
            $backendReady = $true
        }
    } catch {
        $retry++
        if ($retry -lt $maxRetries) {
            Write-Host "   ⏳ Tentative $retry/$maxRetries..." -ForegroundColor Gray
            Start-Sleep -Seconds 3
        }
    }
}

if (-not $backendReady) {
    Write-Host "   ⚠️  Le backend ne répond pas encore" -ForegroundColor Yellow
    Write-Host "   💡 Vérifiez la fenêtre backend pour voir les erreurs" -ForegroundColor Cyan
    Write-Host "   ⏭️  On continue quand même avec ngrok..." -ForegroundColor Yellow
}

# Démarrer ngrok dans une nouvelle fenêtre
Write-Host "`n4️⃣ Démarrage de ngrok dans une nouvelle fenêtre..." -ForegroundColor Yellow
$ngrokCommand = "Write-Host '🌐 Ngrok démarre...' -ForegroundColor Green; Write-Host ''; Write-Host 'Attendez que l URL s affiche ci-dessous...' -ForegroundColor Yellow; Write-Host ''; ngrok http 3001"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $ngrokCommand

Write-Host "   ✅ Fenêtre ngrok ouverte" -ForegroundColor Green
Write-Host "   👀 Regardez la fenêtre ngrok pour voir l'URL (ex: https://abc123.ngrok-free.app)" -ForegroundColor Cyan

# Attendre et récupérer l'URL ngrok
Write-Host "`n5️⃣ Attente de l'URL ngrok..." -ForegroundColor Yellow
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
        $ngrokUrl = $manualUrl.Trim()
        Write-Host "   ✅ URL manuelle: $ngrokUrl" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Aucune URL fournie. Arrêt." -ForegroundColor Red
        exit 1
    }
}

# Mettre à jour les fichiers OpenAPI
Write-Host "`n6️⃣ Mise à jour des fichiers OpenAPI avec l'URL ngrok..." -ForegroundColor Yellow

$files = @(
    "appPackage/apiSpecificationFile/openapi.yaml",
    "appPackage/apiSpecificationFile/openapi_1.yaml",
    "appPackage/apiSpecificationFile/openapi_2.yaml",
    "appPackage/apiSpecificationFile/openapi_3.yaml"
)

$updatedCount = 0
foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        $newContent = $content
        
        # Remplacer localhost et autres URLs
        $patterns = @(
            'http://localhost:3001',
            'https://localhost:3001',
            'http://127.0.0.1:3001',
            'https://127.0.0.1:3001'
        )
        
        $fileUpdated = $false
        foreach ($pattern in $patterns) {
            if ($newContent -match $pattern) {
                $newContent = $newContent -replace [regex]::Escape($pattern), $ngrokUrl
                $fileUpdated = $true
            }
        }
        
        # Remplacer aussi les anciennes URLs ngrok
        if ($newContent -match 'https://[a-z0-9]+\.ngrok-free\.app' -or $newContent -match 'https://[a-z0-9]+\.ngrok\.io') {
            $newContent = $newContent -replace 'https://[a-z0-9]+\.(ngrok-free\.app|ngrok\.io)', $ngrokUrl
            $fileUpdated = $true
        }
        
        if ($fileUpdated) {
            Set-Content -Path $file -Value $newContent -NoNewline -Encoding UTF8
            Write-Host "   ✅ $file" -ForegroundColor Green
            $updatedCount++
        } else {
            Write-Host "   ⏭️  $file (déjà à jour ou pas de remplacement nécessaire)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  $file (introuvable)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✨ Configuration terminée!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Résumé:" -ForegroundColor Cyan
Write-Host "   🌐 URL ngrok: $ngrokUrl" -ForegroundColor White
Write-Host "   📝 Fichiers OpenAPI mis à jour: $updatedCount" -ForegroundColor White
Write-Host ""
Write-Host "📦 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Dans Teams Toolkit, cliquez sur 'Provision' ou 'Deploy' pour rebuilder le ZIP" -ForegroundColor White
Write-Host "   2. Ouvrez Teams Desktop" -ForegroundColor White
Write-Host "   3. Apps → Manage your apps → Upload a custom app" -ForegroundColor White
Write-Host "   4. Sélectionnez: appPackage/build/appPackage.dev.zip" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "   - Gardez ngrok ET le backend en cours d execution pendant vos tests!" -ForegroundColor Yellow
Write-Host "   - L URL ngrok change a chaque redemarrage" -ForegroundColor Yellow
Write-Host "   - Relancez ce script si vous redemarrez ngrok" -ForegroundColor Yellow

