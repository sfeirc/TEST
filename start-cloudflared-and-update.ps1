# Script pour démarrer cloudflared ET mettre à jour automatiquement les fichiers OpenAPI
# Usage: .\start-cloudflared-and-update.ps1

Write-Host "🚀 Démarrage de Cloudflared (alternative a ngrok)" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le backend tourne
Write-Host "1️⃣ Vérification du backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Backend en cours d execution" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend non accessible. Lancez-le d'abord:" -ForegroundColor Yellow
    Write-Host "      cd backend" -ForegroundColor Cyan
    Write-Host "      py -m uvicorn main:app --port 3001" -ForegroundColor Cyan
    exit 1
}

# Vérifier/Installer cloudflared
Write-Host "`n2️⃣ Vérification de Cloudflared..." -ForegroundColor Yellow
$cloudflaredInstalled = Get-Command cloudflared -ErrorAction SilentlyContinue

if (-not $cloudflaredInstalled) {
    Write-Host "   📥 Installation de Cloudflared..." -ForegroundColor Cyan
    
    $cloudflaredPath = "$env:USERPROFILE\cloudflared.exe"
    
    if (-not (Test-Path $cloudflaredPath)) {
        Write-Host "   📥 Téléchargement de Cloudflared..." -ForegroundColor Yellow
        $downloadUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        
        try {
            Invoke-WebRequest -Uri $downloadUrl -OutFile $cloudflaredPath -ErrorAction Stop
            Write-Host "   ✅ Cloudflared téléchargé" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Erreur lors du téléchargement" -ForegroundColor Red
            Write-Host "   💡 Téléchargez manuellement depuis:" -ForegroundColor Yellow
            Write-Host "      https://github.com/cloudflare/cloudflared/releases" -ForegroundColor Cyan
            Write-Host "   💡 Ou utilisez Chocolatey: choco install cloudflared" -ForegroundColor Cyan
            exit 1
        }
    }
    
    $cloudflaredCmd = $cloudflaredPath
} else {
    Write-Host "   ✅ Cloudflared deja installe" -ForegroundColor Green
    $cloudflaredCmd = "cloudflared"
}

# Démarrer cloudflared dans une nouvelle fenêtre
Write-Host "`n3️⃣ Démarrage de Cloudflared dans une nouvelle fenetre..." -ForegroundColor Yellow
$cloudflaredCommand = "Write-Host 'Cloudflared demarre!' -ForegroundColor Green; Write-Host ''; Write-Host 'Attendez que l URL s affiche ci-dessous...' -ForegroundColor Yellow; Write-Host ''; $cloudflaredCmd tunnel --url http://localhost:3001"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $cloudflaredCommand

Write-Host "   ✅ Fenetre Cloudflared ouverte" -ForegroundColor Green
Write-Host "   👀 Regardez la fenetre pour voir l URL (ex: https://xxxxx.trycloudflare.com)" -ForegroundColor Cyan

# Attendre et demander l'URL (cloudflared n'a pas d'API comme ngrok)
Write-Host "`n4️⃣ Attente de l URL Cloudflared..." -ForegroundColor Yellow
Write-Host "   ⏳ Attendez 5-10 secondes que l URL s affiche dans la fenetre Cloudflared" -ForegroundColor Gray
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "💡 Copiez l URL depuis la fenetre Cloudflared" -ForegroundColor Cyan
Write-Host "   Format attendu: https://xxxxx.trycloudflare.com" -ForegroundColor Gray
$cloudflaredUrl = Read-Host "Entrez l URL Cloudflared"

if (-not $cloudflaredUrl) {
    Write-Host "❌ Aucune URL fournie. Arret." -ForegroundColor Red
    exit 1
}

# Nettoyer l'URL (enlever les espaces, etc.)
$cloudflaredUrl = $cloudflaredUrl.Trim()

# Mettre à jour les fichiers OpenAPI
Write-Host "`n5️⃣ Mise a jour des fichiers OpenAPI avec l URL Cloudflared..." -ForegroundColor Yellow

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
                $newContent = $newContent -replace [regex]::Escape($pattern), $cloudflaredUrl
                $fileUpdated = $true
            }
        }
        
        # Remplacer aussi les anciennes URLs (ngrok, cloudflared, etc.)
        if ($newContent -match 'https://[a-z0-9-]+\.(ngrok-free\.app|ngrok\.io|trycloudflare\.com)') {
            $newContent = $newContent -replace 'https://[a-z0-9-]+\.(ngrok-free\.app|ngrok\.io|trycloudflare\.com)', $cloudflaredUrl
            $fileUpdated = $true
        }
        
        if ($fileUpdated) {
            Set-Content -Path $file -Value $newContent -NoNewline -Encoding UTF8
            Write-Host "   ✅ $file" -ForegroundColor Green
            $updatedCount++
        } else {
            Write-Host "   ⏭️  $file (deja a jour ou pas de remplacement necessaire)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  $file (introuvable)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✨ Configuration terminee!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Resume:" -ForegroundColor Cyan
Write-Host "   🌐 URL Cloudflared: $cloudflaredUrl" -ForegroundColor White
Write-Host "   📝 Fichiers OpenAPI mis a jour: $updatedCount" -ForegroundColor White
Write-Host ""
Write-Host "📦 Prochaines etapes:" -ForegroundColor Cyan
Write-Host "   1. Dans Teams Toolkit, cliquez sur 'Provision' ou 'Deploy' pour rebuilder le ZIP" -ForegroundColor White
Write-Host "   2. Ouvrez Teams Desktop" -ForegroundColor White
Write-Host "   3. Apps → Manage your apps → Upload a custom app" -ForegroundColor White
Write-Host "   4. Selectionnez: appPackage/build/appPackage.dev.zip" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "   - Gardez Cloudflared ET le backend en cours d execution pendant vos tests!" -ForegroundColor Yellow
Write-Host "   - L URL Cloudflared change a chaque redemarrage" -ForegroundColor Yellow
Write-Host "   - Relancez ce script si vous redemarrez Cloudflared" -ForegroundColor Yellow
Write-Host ""

