# 🚀 Démarrage Rapide avec ngrok

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

### 2. Démarrer ngrok (Terminal 2)

Ouvrez un **nouveau** terminal PowerShell et lancez:

```powershell
.\start-ngrok-and-update.ps1
```

Le script va:
- ✅ Vérifier que le backend tourne
- ✅ Démarrer ngrok dans une nouvelle fenêtre
- ✅ Détecter automatiquement l'URL ngrok
- ✅ Mettre à jour tous les fichiers OpenAPI

### 3. Rebuild Teams Package

Dans Teams Toolkit (VS Code):
- Cliquez sur "Provision" ou "Deploy"
- Ou rebuild manuel: le ZIP sera créé dans `appPackage/build/appPackage.dev.zip`

### 4. Upload dans Teams

1. Ouvrez Teams Desktop
2. Apps → Manage your apps
3. Upload a custom app
4. Sélectionnez: `appPackage/build/appPackage.dev.zip`

### 5. Tester!

Ouvrez votre agent dans Teams et testez une action.

---

## ⚠️ Important

- **Gardez les 2 fenêtres ouvertes** (backend + ngrok) pendant vos tests
- L'URL ngrok change à chaque redémarrage
- Si vous redémarrez ngrok, relancez `start-ngrok-and-update.ps1`

---

## 🐛 Dépannage

### Backend ne démarre pas
- Vérifiez que vous avez un fichier `.env` dans `backend/`
- Vérifiez les dépendances: `pip install -r backend/requirements.txt`

### ngrok non trouvé
- Lancez: `.\setup-ngrok.ps1`

### URL ngrok non détectée
- Le script vous demandera de l'entrer manuellement
- Copiez l'URL depuis la fenêtre ngrok (ex: `https://abc123.ngrok-free.app`)

