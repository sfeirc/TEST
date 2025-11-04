# 🧪 Tester l'Agent dans Teams Desktop (Local)

## Problème
Teams Desktop ne peut pas accéder à `localhost:3001`. Il faut exposer votre backend publiquement.

## Solution : Utiliser ngrok

### 1. Installer ngrok
```bash
# Windows (avec winget ou Chocolatey)
winget install ngrok

# Ou télécharger depuis: https://ngrok.com/download
```

### 2. Démarrer votre backend
```bash
cd backend
py -m uvicorn main:app --port 3001
```

### 3. Exposer avec ngrok (dans un autre terminal)
```bash
ngrok http 3001
```

Vous obtiendrez une URL comme : `https://abc123.ngrok-free.app`

### 4. Mettre à jour les fichiers OpenAPI

**Option A : Modifier manuellement** (pour un test rapide)

Remplacez `http://localhost:3001` par votre URL ngrok dans :
- `appPackage/apiSpecificationFile/openapi.yaml`
- `appPackage/apiSpecificationFile/openapi_1.yaml`
- `appPackage/apiSpecificationFile/openapi_2.yaml`
- `appPackage/apiSpecificationFile/openapi_3.yaml`

**Option B : Utiliser le script** (recommandé)

Voir section ci-dessous.

### 5. Rebuild le ZIP
```bash
# Dans Teams Toolkit, cliquez sur "Provision" ou "Deploy"
# Cela va rebuilder le ZIP avec les nouvelles URLs
```

### 6. Importer dans Teams Desktop
1. Ouvrez Teams Desktop
2. Apps → Manage your apps → Upload a custom app
3. Sélectionnez : `appPackage/build/appPackage.dev.zip`
4. Testez votre agent !

---

## ⚠️ Important

- **Gardez ngrok ET le backend en cours d'exécution** pendant vos tests
- L'URL ngrok change à chaque redémarrage (gratuit) ou reste fixe (plan payant)
- Pour production, utilisez un hébergement permanent (Azure App Service, etc.)

---

## 🔄 Script automatique (Optionnel)

Créez un script `update-ngrok-url.ps1` pour automatiser la mise à jour :

```powershell
# Récupérer l'URL ngrok depuis l'API ngrok locale
$ngrokUrl = (Invoke-RestMethod http://127.0.0.1:4040/api/tunnels).tunnels[0].public_url

# Mettre à jour tous les fichiers OpenAPI
$files = @(
    "appPackage/apiSpecificationFile/openapi.yaml",
    "appPackage/apiSpecificationFile/openapi_1.yaml",
    "appPackage/apiSpecificationFile/openapi_2.yaml",
    "appPackage/apiSpecificationFile/openapi_3.yaml"
)

foreach ($file in $files) {
    (Get-Content $file) -replace 'http://localhost:3001', $ngrokUrl | Set-Content $file
    Write-Host "Updated $file with $ngrokUrl"
}
```

Puis exécutez après avoir lancé ngrok :
```powershell
.\update-ngrok-url.ps1
```

