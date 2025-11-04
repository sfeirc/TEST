# Script pour mettre à jour les URLs dans les fichiers OpenAPI
# Usage: .\update-openapi-url.ps1 -NewUrl "https://your-backend-url.com"

param(
    [Parameter(Mandatory=$true)]
    [string]$NewUrl
)

Write-Host "🔄 Mise à jour des fichiers OpenAPI avec la nouvelle URL..." -ForegroundColor Cyan
Write-Host "   Nouvelle URL: $NewUrl" -ForegroundColor Yellow
Write-Host ""

# Liste des fichiers OpenAPI à mettre à jour
$files = @(
    "appPackage/apiSpecificationFile/openapi.yaml",
    "appPackage/apiSpecificationFile/openapi_1.yaml",
    "appPackage/apiSpecificationFile/openapi_2.yaml",
    "appPackage/apiSpecificationFile/openapi_3.yaml"
)

$updatedCount = 0
$patterns = @(
    "http://localhost:3001",
    "https://localhost:3001",
    "http://127.0.0.1:3001",
    "https://127.0.0.1:3001"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        $newContent = $content
        $fileUpdated = $false
        
        foreach ($pattern in $patterns) {
            if ($newContent -match $pattern) {
                $newContent = $newContent -replace [regex]::Escape($pattern), $NewUrl
                $fileUpdated = $true
            }
        }
        
        # Also replace any ngrok URLs
        if ($newContent -match 'https://[a-z0-9]+\.ngrok-free\.app' -or $newContent -match 'https://[a-z0-9]+\.ngrok\.io') {
            $newContent = $newContent -replace 'https://[a-z0-9]+\.(ngrok-free\.app|ngrok\.io)', $NewUrl
            $fileUpdated = $true
        }
        
        # Also replace cloudflare tunnel URLs
        if ($newContent -match 'https://[a-z0-9-]+\.trycloudflare\.com') {
            $newContent = $newContent -replace 'https://[a-z0-9-]+\.trycloudflare\.com', $NewUrl
            $fileUpdated = $true
        }
        
        if ($fileUpdated) {
            Set-Content -Path $file -Value $newContent -NoNewline -Encoding UTF8
            Write-Host "   ✅ $file" -ForegroundColor Green
            $updatedCount++
        } else {
            Write-Host "   ⏭️  $file (aucune URL trouvée à remplacer)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  $file (introuvable)" -ForegroundColor Yellow
    }
}

Write-Host ""
if ($updatedCount -gt 0) {
    Write-Host "✨ $updatedCount fichier(s) mis à jour avec succès!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Prochaines étapes:" -ForegroundColor Cyan
    Write-Host "   1. Rebuild le package Teams: dans Teams Toolkit, cliquez sur 'Provision' ou 'Deploy'" -ForegroundColor White
    Write-Host "   2. Le nouveau ZIP sera dans: appPackage/build/appPackage.dev.zip" -ForegroundColor White
    Write-Host "   3. Upload dans Teams: Apps → Manage your apps → Upload a custom app" -ForegroundColor White
} else {
    Write-Host "⚠️  Aucun fichier n'a été mis à jour" -ForegroundColor Yellow
}

