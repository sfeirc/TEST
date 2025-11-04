# 🔄 Alternatives à ngrok pour tester Teams Desktop

Si ngrok ne fonctionne pas, voici plusieurs alternatives :

## Option 1 : Cloudflared (Cloudflare Tunnel) ⭐ RECOMMANDÉ

**Avantages :**
- ✅ Gratuit et illimité
- ✅ Plus stable que ngrok parfois
- ✅ Pas besoin de compte
- ✅ URLs temporaires (changent à chaque redémarrage)

**Installation rapide :**
```powershell
.\setup-cloudflared.ps1
```

**Installation manuelle :**
1. Téléchargez depuis : https://github.com/cloudflare/cloudflared/releases
2. Extrayez `cloudflared.exe` dans `C:\Users\VotreNom\`
3. Lancez : `cloudflared tunnel --url http://localhost:3001`
4. Copiez l'URL affichée (ex: `https://xxxxx.trycloudflare.com`)

---

## Option 2 : Hébergement Azure App Service (Permanent) ⭐⭐ POUR PRODUCTION

**Avantages :**
- ✅ URL permanente et stable
- ✅ HTTPS automatique
- ✅ Pas de limitation de temps
- ✅ Intégration native avec Azure OpenAI

**Déploiement :**
1. Créez un Azure App Service (Linux, Python 3.11)
2. Déployez votre backend
3. Configurez les variables d'environnement
4. Utilisez l'URL Azure : `https://votre-app.azurewebsites.net`

**Note :** Vous avez déjà une demande d'hébergement en cours avec l'IT. C'est la meilleure solution pour la production.

---

## Option 3 : Tester le backend seul (sans Teams Desktop)

**Pour valider que votre backend fonctionne :**

1. Lancez le backend :
```powershell
cd backend
py -m uvicorn main:app --port 3001
```

2. Testez avec Swagger :
   - Ouvrez : http://localhost:3001/docs
   - Testez tous les endpoints manuellement

3. Testez avec Postman :
   - Importez les endpoints depuis `appPackage/apiSpecificationFile/openapi.yaml`
   - Testez les appels API

**Limitation :** Vous ne pourrez pas tester les Adaptive Cards de Teams, mais vous validerez que l'API fonctionne.

---

## Option 4 : Utiliser localtunnel

**Installation :**
```powershell
npm install -g localtunnel
```

**Utilisation :**
```powershell
lt --port 3001
```

**Note :** Nécessite Node.js installé.

---

## Option 5 : Serveo (SSH tunnel)

**Utilisation :**
```powershell
ssh -R 80:localhost:3001 serveo.net
```

**Note :** Nécessite SSH (disponible sur Windows 10+ avec OpenSSH).

---

## 🔍 Comparaison rapide

| Solution | Gratuit | Stable | Permanent | Installation |
|----------|---------|--------|-----------|-------------|
| Cloudflared | ✅ | ✅✅ | ❌ | Facile |
| Azure App Service | ❌ | ✅✅✅ | ✅ | Moyenne |
| localtunnel | ✅ | ✅ | ❌ | Facile (si Node.js) |
| Serveo | ✅ | ✅ | ❌ | Facile (si SSH) |

---

## 💡 Recommandation

**Pour tester rapidement :**
→ Utilisez **Cloudflared** (Option 1)

**Pour production :**
→ Utilisez **Azure App Service** (Option 2) - votre demande IT est en cours

**Pour valider le backend :**
→ Testez avec **Swagger/Postman** (Option 3) en local

---

## 🚀 Quick Start avec Cloudflared

```powershell
# 1. Lancer le backend
cd backend
py -m uvicorn main:app --port 3001

# 2. Dans un autre terminal, lancer le script
.\setup-cloudflared.ps1

# 3. Rebuild le ZIP dans Teams Toolkit
# 4. Importer dans Teams Desktop
```

