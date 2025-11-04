# ⚡ Déploiement Rapide - 5 Minutes

## Option la Plus Simple: Render.com

### 1. Préparer votre code sur GitHub

```powershell
# Si ce n'est pas déjà fait
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/INFOTEL.git
git push -u origin main
```

### 2. Déployer sur Render

1. Allez sur https://render.com
2. Créez un compte (gratuit)
3. "New +" → "Web Service"
4. Connectez votre repo GitHub
5. Configurez:
   - **Name:** `infotel-ai-backend`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

6. Dans "Environment Variables", ajoutez:
   ```
   PORT=8000
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_KEY=your-key
   AZURE_OPENAI_DEPLOYMENT=gpt-5
   ```

7. Cliquez "Create Web Service"
8. Attendez 2-3 minutes
9. Copiez l'URL: `https://infotel-ai-backend.onrender.com`

### 3. Mettre à jour Teams

```powershell
.\update-openapi-url.ps1 -NewUrl "https://infotel-ai-backend.onrender.com"
```

### 4. Rebuild et Upload dans Teams

- Dans Teams Toolkit: `Provision` ou `Deploy`
- Teams Desktop → Apps → Manage your apps → Upload custom app
- Sélectionnez: `appPackage/build/appPackage.dev.zip`

### 5. Tester

Ouvrez votre agent dans Teams et testez une action!

---

## 🔄 Alternative: Garder sur votre PC avec ngrok

Si vous voulez juste tester sans déployer:

```powershell
# Terminal 1: Démarrer le backend
cd backend
py -m uvicorn main:app --port 3001

# Terminal 2: Démarrer ngrok et mettre à jour
.\start-ngrok-and-update.ps1
```

Puis rebuild Teams et upload le ZIP.

**Note:** ngrok change l'URL à chaque redémarrage. Pour production, utilisez Render ou Azure.

