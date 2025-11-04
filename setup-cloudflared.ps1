# Script pour utiliser Cloudflared au lieu de ngrok
# Installation et configuration automatique

Write-Host "🚀 Configuration de Cloudflared (alternative a ngrok)" -ForegroundColor Cyan
Write-Host ""

# Vérifier si cloudflared est installé
Write-Host "1️⃣ Vérification de Cloudflared..." -ForegroundColor Yellow
$cloudflaredInstalled = Get-Command cloudflared -ErrorAction SilentlyContinue

if (-not $cloudflaredInstalled) {
    Write-Host "   📥 Installation de Cloudflared..." -ForegroundColor Cyan
    
    # Télécharger cloudflared
    $downloadUrl = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    $cloudflaredPath = "$env:USERPROFILE\cloudflared.exe"
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $cloudflaredPath -ErrorAction Stop
        Write-Host "   ✅ Cloudflared téléchargé" -ForegroundColor Green
        
        # Ajouter au PATH de la session
        $env:Path += ";$env:USERPROFILE"
        
        Write-Host "   ✅ Cloudflared installé dans: $cloudflaredPath" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Erreur lors du téléchargement" -ForegroundColor Red
        Write-Host "   💡 Téléchargez manuellement depuis: https://github.com/cloudflare/cloudflared/releases" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "   ✅ Cloudflared déjà installé" -ForegroundColor Green
}

# Vérifier le backend
Write-Host "`n2️⃣ Vérification du backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Backend en cours d'exécution" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend non accessible. Lancez-le d'abord:" -ForegroundColor Yellow
    Write-Host "      cd backend && py -m uvicorn main:app --port 3001" -ForegroundColor Cyan
    exit 1
}

# Démarrer cloudflared
Write-Host "`n3️⃣ Démarrage de Cloudflared..." -ForegroundColor Yellow

if ($cloudflaredInstalled) {
    $cloudflaredCmd = "cloudflared"
} else {
    $cloudflaredCmd = "$env:USERPROFILE\cloudflared.exe"
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Cloudflared demarre!' -ForegroundColor Green; Write-Host ''; Write-Host 'Attendez que l URL s affiche...' -ForegroundColor Yellow; Write-Host ''; $cloudflaredCmd tunnel --url http://localhost:3001"

Write-Host "   ✅ Fenêtre Cloudflared ouverte" -ForegroundColor Green
Write-Host "   👀 Regardez la fenêtre pour voir l'URL (ex: https://xxxxx.trycloudflare.com)" -ForegroundColor Cyan

Write-Host "`n⏳ Attente de l'URL Cloudflared..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Essayer de récupérer l'URL (cloudflared n'a pas d'API comme ngrok, donc on demande à l'utilisateur)
Write-Host "`n💡 Copiez l'URL depuis la fenêtre Cloudflared (ex: https://xxxxx.trycloudflare.com)" -ForegroundColor Cyan
$cloudflaredUrl = Read-Host "Entrez l'URL Cloudflared"

if (-not $cloudflaredUrl) {
    Write-Host "❌ Aucune URL fournie. Arrêt." -ForegroundColor Red
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
        $newContent = $content -replace 'http://localhost:3001', $cloudflaredUrl
        
        if ($content -ne $newContent) {
            Set-Content -Path $file -Value $newContent -NoNewline
            Write-Host "   ✅ $file" -ForegroundColor Green
            $updatedCount++
        }
    }
}

Write-Host "`n✨ Configuration terminée!" -ForegroundColor Green
Write-Host "   📋 URL utilisée: $cloudflaredUrl" -ForegroundColor Gray
Write-Host "   📦 Prochaine étape: Rebuild le ZIP avec Teams Toolkit (Provision ou Deploy)" -ForegroundColor Cyan

