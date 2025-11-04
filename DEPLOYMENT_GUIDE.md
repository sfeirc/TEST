# 🚀 Guide de Déploiement - Backend INFOTEL AI

Ce guide vous montre comment publier votre backend FastAPI en ligne pour que Teams puisse y accéder.

---

## 🎯 Options de Déploiement

### Option 1: Render.com (⭐ RECOMMANDÉ - Gratuit et Simple)

**Avantages:**
- ✅ Gratuit (tier gratuit disponible)
- ✅ HTTPS automatique
- ✅ Déploiement en 5 minutes
- ✅ Variables d'environnement sécurisées
- ✅ Auto-rebuild sur Git push

**Étapes:**

1. **Créer un compte Render:**
   - Allez sur https://render.com
   - Créez un compte (gratuit avec GitHub/Google)

2. **Déployer le service:**
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre repository GitHub (ou créez-en un)
   - Configuration:
     - **Name:** `infotel-ai-backend`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Start Command:** `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan:** Free

3. **Configurer les variables d'environnement:**
   - Dans Render Dashboard → Environment
   - Ajoutez toutes vos variables depuis `backend/.env`:
     ```
     PORT=8000
     AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
     AZURE_OPENAI_KEY=your-key
     AZURE_OPENAI_DEPLOYMENT=gpt-5
     ```

4. **Déployer:**
   - Cliquez "Create Web Service"
   - Attendez 2-3 minutes
   - Votre URL sera: `https://infotel-ai-backend.onrender.com`

5. **Mettre à jour Teams:**
   ```powershell
   .\update-openapi-url.ps1 -NewUrl "https://infotel-ai-backend.onrender.com"
   ```

---

### Option 2: Railway.app (⭐ Alternative Gratuite)

**Avantages:**
- ✅ Gratuit ($5 crédit/mois)
- ✅ Très simple
- ✅ Déploiement automatique

**Étapes:**

1. **Créer un compte:**
   - https://railway.app
   - Connectez avec GitHub

2. **Déployer:**
   - "New Project" → "Deploy from GitHub repo"
   - Sélectionnez votre repo
   - Railway détecte automatiquement Python
   - Configurez les variables d'environnement dans "Variables"

3. **Récupérer l'URL:**
   - Railway génère une URL automatiquement
   - Ex: `https://infotel-ai-backend-production.up.railway.app`

4. **Mettre à jour Teams:**
   ```powershell
   .\update-openapi-url.ps1 -NewUrl "https://votre-url-railway.railway.app"
   ```

---

### Option 3: Azure App Service (⭐ Pour Production Entreprise)

**Avantages:**
- ✅ Intégration native Azure OpenAI
- ✅ Monitoring Application Insights
- ✅ Scaling automatique
- ✅ HTTPS automatique

**Étapes:**

1. **Prérequis:**
   - Azure CLI installé
   - Compte Azure avec accès

2. **Créer l'App Service:**
   ```powershell
   # Créer un resource group
   az group create --name infotel-ai-rg --location westeurope

   # Créer l'App Service Plan
   az appservice plan create --name infotel-ai-plan --resource-group infotel-ai-rg --sku FREE --is-linux

   # Créer l'App Service
   az webapp create --resource-group infotel-ai-rg --plan infotel-ai-plan --name infotel-ai-backend --runtime "PYTHON:3.11"

   # Configurer le démarrage
   az webapp config set --resource-group infotel-ai-rg --name infotel-ai-backend --startup-file "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
   ```

3. **Configurer les variables d'environnement:**
   ```powershell
   az webapp config appsettings set --resource-group infotel-ai-rg --name infotel-ai-backend --settings PORT=8000 AZURE_OPENAI_ENDPOINT="..." AZURE_OPENAI_KEY="..."
   ```

4. **Déployer le code:**
   ```powershell
   # Via Git deploy (recommandé)
   az webapp deployment source config --name infotel-ai-backend --resource-group infotel-ai-rg --repo-url https://github.com/votre-repo --branch main --manual-integration

   # OU via ZIP
   cd backend
   zip -r deploy.zip .
   az webapp deployment source config-zip --resource-group infotel-ai-rg --name infotel-ai-backend --src deploy.zip
   ```

5. **Récupérer l'URL:**
   - URL sera: `https://infotel-ai-backend.azurewebsites.net`

6. **Mettre à jour Teams:**
   ```powershell
   .\update-openapi-url.ps1 -NewUrl "https://infotel-ai-backend.azurewebsites.net"
   ```

---

### Option 4: Local avec ngrok (Pour Tests Rapides)

**Avantages:**
- ✅ Pas de déploiement
- ✅ Test immédiat
- ⚠️ URL change à chaque redémarrage
- ⚠️ Nécessite PC allumé

**Étapes:**

1. **Démarrer le backend local:**
   ```powershell
   cd backend
   py -m uvicorn main:app --port 3001
   ```

2. **Démarrer ngrok:**
   ```powershell
   .\start-ngrok-and-update.ps1
   ```

3. **Le script met à jour automatiquement les fichiers OpenAPI**

---

## 📋 Checklist Post-Déploiement

Après avoir déployé, vérifiez:

1. ✅ **Health Check:**
   ```powershell
   Invoke-WebRequest -Uri "https://votre-url.com/health"
   ```

2. ✅ **Mise à jour OpenAPI:**
   ```powershell
   .\update-openapi-url.ps1 -NewUrl "https://votre-url.com"
   ```

3. ✅ **Rebuild Teams Package:**
   - Dans Teams Toolkit: `Provision` ou `Deploy`
   - Ou rebuild manuel: le ZIP sera dans `appPackage/build/appPackage.dev.zip`

4. ✅ **Upload dans Teams:**
   - Teams Desktop → Apps → Manage your apps
   - Upload a custom app
   - Sélectionnez `appPackage/build/appPackage.dev.zip`

5. ✅ **Tester dans Teams:**
   - Ouvrez votre agent
   - Testez une action (ex: analyser un RFP)

---

## 🔧 Configuration Requise

### Variables d'Environnement Minimales

```env
PORT=8000
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_DEPLOYMENT=gpt-5
```

### Variables Optionnelles

```env
# SharePoint (si utilisé)
SHAREPOINT_CLIENT_ID=...
SHAREPOINT_CLIENT_SECRET=...
SHAREPOINT_TENANT_ID=...
```

---

## 🐛 Dépannage

### Le backend ne démarre pas

- Vérifiez les logs dans le dashboard de votre hébergeur
- Vérifiez que `PORT` est configuré (Render utilise `$PORT` automatiquement)
- Vérifiez que toutes les dépendances sont dans `requirements.txt`

### Teams ne peut pas appeler l'API

- Vérifiez que l'URL est en HTTPS (obligatoire pour Teams)
- Vérifiez que CORS est configuré (déjà fait dans `main.py`)
- Vérifiez que les fichiers OpenAPI sont à jour avec la bonne URL

### Erreur 500 sur les endpoints

- Vérifiez les variables d'environnement (Azure OpenAI keys)
- Vérifiez les logs du serveur
- Testez avec `/health` d'abord

---

## 📞 Support

Pour toute question, consultez:
- `PROCEDURE_HEBERGEMENT.md` - Documentation technique détaillée
- `backend/README.md` - Documentation du backend
- Logs de votre hébergeur

