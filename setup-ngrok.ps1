# Script pour configurer ngrok et mettre à jour les fichiers OpenAPI
# Usage: .\setup-ngrok.ps1

Write-Host "🚀 Configuration ngrok pour Teams Desktop" -ForegroundColor Cyan
Write-Host ""

# Vérifier que ngrok est installé
Write-Host "1️⃣ Vérification de ngrok..." -ForegroundColor Yellow
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "   ✅ Ngrok est installé" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Ngrok n'est pas installé. Installez-le avec: winget install Ngrok.Ngrok" -ForegroundColor Red
    exit 1
}

# Vérifier que le backend tourne
Write-Host "`n2️⃣ Vérification du backend sur le port 3001..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Backend est en cours d'exécution" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend n'est pas accessible sur le port 3001" -ForegroundColor Yellow
    Write-Host "   💡 Lancez le backend avec: cd backend && py -m uvicorn main:app --port 3001" -ForegroundColor Cyan
    $continue = Read-Host "   Continuer quand même ? (o/n)"
    if ($continue -ne "o") { exit 1 }
}

# Instructions pour lancer ngrok
Write-Host "`n3️⃣ Lancement de ngrok..." -ForegroundColor Yellow
Write-Host "   📋 Ouvrez un NOUVEAU terminal PowerShell et exécutez:" -ForegroundColor Cyan
Write-Host "      ngrok http 3001" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "   ⏳ Attendez que ngrok affiche l'URL (ex: https://abc123.ngrok-free.app)" -ForegroundColor Gray
Write-Host ""

# Attendre que ngrok soit accessible
$maxRetries = 20
$retry = 0
$ngrokUrl = $null

Write-Host "   🔍 Attente de ngrok..." -ForegroundColor Yellow
while ($retry -lt $maxRetries -and -not $ngrokUrl) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
        if ($response.tunnels.Count -gt 0) {
            $ngrokUrl = $response.tunnels[0].public_url
            Write-Host "   ✅ URL ngrok trouvée: $ngrokUrl" -ForegroundColor Green
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
    Write-Host "   ❌ Ngrok n'est pas accessible après $maxRetries tentatives" -ForegroundColor Red
    Write-Host "   💡 Vérifiez que vous avez bien lancé 'ngrok http 3001' dans un autre terminal" -ForegroundColor Yellow
    exit 1
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
Write-Host "   ⚠️  IMPORTANT: Gardez ngrok ET le backend en cours d'exécution pendant vos tests!" -ForegroundColor Yellow

