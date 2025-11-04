# 🚀 Démarrage avec Cloudflared (Alternative à ngrok)

Cloudflared (Cloudflare Tunnel) est souvent **non bloqué** par les entreprises car c'est un outil Cloudflare.

## Étapes Simples

### 1. Démarrer le Backend (Terminal 1)

Ouvrez un terminal PowerShell et lancez:

```powershell
cd backend
py -m uvicorn main:app --port 3001
```

Laissez cette fenêtre ouverte. Vous devriez voir:
```
INFO:     Uvicorn running on http://0.0.0.0:3001
```

### 2. Démarrer Cloudflared (Terminal 2)

Ouvrez un **nouveau** terminal PowerShell et lancez:

```powershell
.\start-cloudflared-and-update.ps1
```

Le script va:
- ✅ Installer Cloudflared automatiquement (si nécessaire)
- ✅ Démarrer Cloudflared dans une nouvelle fenêtre
- ✅ Vous demander de copier l'URL (ex: `https://xxxxx.trycloudflare.com`)
- ✅ Mettre à jour automatiquement tous les fichiers OpenAPI

### 3. Rebuild Teams Package

Dans Teams Toolkit (VS Code):
- Cliquez sur "Provision" ou "Deploy"
- Le ZIP sera créé dans `appPackage/build/appPackage.dev.zip`

### 4. Upload dans Teams

1. Ouvrez Teams Desktop
2. Apps → Manage your apps
3. Upload a custom app
4. Sélectionnez: `appPackage/build/appPackage.dev.zip`

### 5. Tester!

Ouvrez votre agent dans Teams et testez une action.

---

## ⚠️ Important

- **Gardez les 2 fenêtres ouvertes** (backend + Cloudflared) pendant vos tests
- L'URL Cloudflared change à chaque redémarrage
- Si vous redémarrez Cloudflared, relancez `start-cloudflared-and-update.ps1`

---

## 🐛 Dépannage

### Cloudflared ne télécharge pas
- Téléchargez manuellement: https://github.com/cloudflare/cloudflared/releases
- Extrayez `cloudflared-windows-amd64.exe` dans `C:\Users\VotreNom\`
- Renommez-le en `cloudflared.exe`

### Backend ne démarre pas
- Vérifiez que vous avez un fichier `.env` dans `backend/`
- Vérifiez les dépendances: `pip install -r backend/requirements.txt`

### URL Cloudflared non visible
- Regardez attentivement la fenêtre Cloudflared
- L'URL apparaît généralement après 5-10 secondes
- Format: `https://xxxxx.trycloudflare.com`

---

## 🎯 Alternative: Hébergement Permanent

Si Cloudflared ne fonctionne pas ou pour la production, déployez en ligne:

- **Render.com** (gratuit): Suivez `QUICK_DEPLOY.md`
- **Azure App Service**: Votre demande IT est en cours

Consultez `DEPLOYMENT_GUIDE.md` pour toutes les options.

