# Script pour mettre à jour automatiquement les URLs ngrok dans les fichiers OpenAPI
# Utilisation: .\update-ngrok-url.ps1

Write-Host "🔍 Recherche de l'URL ngrok..." -ForegroundColor Cyan

try {
    # Récupérer l'URL ngrok depuis l'API ngrok locale
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
    $ngrokUrl = $response.tunnels[0].public_url
    
    if (-not $ngrokUrl) {
        Write-Host "❌ Aucun tunnel ngrok trouvé. Assurez-vous que ngrok est en cours d'exécution." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ URL ngrok trouvée: $ngrokUrl" -ForegroundColor Green
} catch {
    Write-Host "❌ Impossible de se connecter à ngrok. Assurez-vous que ngrok est en cours d'exécution." -ForegroundColor Red
    Write-Host "   Erreur: $_" -ForegroundColor Yellow
    exit 1
}

# Liste des fichiers OpenAPI à mettre à jour
$files = @(
    "appPackage/apiSpecificationFile/openapi.yaml",
    "appPackage/apiSpecificationFile/openapi_1.yaml",
    "appPackage/apiSpecificationFile/openapi_2.yaml",
    "appPackage/apiSpecificationFile/openapi_3.yaml"
)

Write-Host "`n📝 Mise à jour des fichiers OpenAPI..." -ForegroundColor Cyan

$updatedCount = 0
foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $newContent = $content -replace 'http://localhost:3001', $ngrokUrl
        
        if ($content -ne $newContent) {
            Set-Content -Path $file -Value $newContent -NoNewline
            Write-Host "   ✅ Mis à jour: $file" -ForegroundColor Green
            $updatedCount++
        } else {
            Write-Host "   ⏭️  Déjà à jour: $file" -ForegroundColor Gray
        }
    } else {
        Write-Host "   ⚠️  Fichier introuvable: $file" -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Terminé! $updatedCount fichier(s) mis à jour avec $ngrokUrl" -ForegroundColor Green
Write-Host "`n📦 N'oubliez pas de rebuilder le ZIP avec Teams Toolkit (Provision ou Deploy)" -ForegroundColor Cyan

