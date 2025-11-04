# 🎮 Accéder au Teams Playground pour votre Agent Déclaratif

## ⚠️ Important : Différence entre types d'agents

Votre projet utilise un **Agent Déclaratif** (pas un SDK Agent). Il y a deux types d'agents :

### 1. **SDK Agents (Bot Framework)**
- Utilisent le Playground standalone (`agentsplayground` CLI)
- Nécessitent du code Bot Framework
- Testés via `agentsplayground -e "http://localhost:3978/api/messages"`

### 2. **Déclarative Agents** (votre cas)
- Utilisent `declarativeAgent.json`
- Testés via **Copilot** ou **Teams Desktop**
- Pas de Playground standalone direct

---

## 🎯 Solutions pour tester votre Agent Déclaratif

### Option 1 : Preview in Copilot (Équivalent Playground) ⭐ RECOMMANDÉ

**C'est l'équivalent du Playground pour les agents déclaratifs.**

1. Dans VS Code, ouvrez le menu Run and Debug (F5)
2. Sélectionnez **"Preview in Copilot (Chrome)"** ou **"Preview in Copilot (Edge)"**
3. Appuyez sur F5

**Avantages :**
- ✅ Pas besoin de tenant activé
- ✅ Pas besoin de Custom App Upload
- ✅ Test direct dans l'interface Copilot
- ✅ Fonctionne immédiatement après Provision

**Limitation :**
- ❌ Les Adaptive Cards avec boutons ne fonctionnent pas (elles sont pour Teams uniquement)

---

### Option 2 : Teams Desktop (Pour tester les Adaptive Cards)

**Pour tester les Adaptive Cards avec boutons, il FAUT passer par Teams Desktop.**

#### Prérequis :
1. **"Custom App Upload" activé** dans votre tenant
   - OU utiliser le compte admin (`Agent_Presales@3fw0f6.onmicrosoft.com`)
2. **Backend accessible publiquement** (ngrok, cloudflared, ou Azure)

#### Étapes :
1. **Provision** votre app dans Teams Toolkit
2. **Backend accessible** (via ngrok/cloudflared ou Azure)
3. **Mettre à jour les fichiers OpenAPI** avec l'URL publique
4. **Rebuild le ZIP** (Provision ou Deploy)
5. **Importer dans Teams Desktop** :
   - Apps → Manage your apps → Upload a custom app
   - Sélectionnez : `appPackage/build/appPackage.dev.zip`

---

### Option 3 : Convertir en SDK Agent (Complexe)

**Si vous voulez vraiment utiliser le Playground standalone (`agentsplayground`) :**

⚠️ **Attention :** Cela nécessite de réécrire votre agent en Bot Framework SDK.

**Étapes :**
1. Créer un nouveau projet SDK Agent avec Teams Toolkit
2. Migrer votre logique d'agent déclaratif vers Bot Framework
3. Implémenter les Adaptive Cards dans le code
4. Utiliser `agentsplayground` pour tester

**C'est un gros travail et pas recommandé si vous avez déjà un agent déclaratif fonctionnel.**

---

## 📋 Recommandation selon votre besoin

| Besoin | Solution |
|--------|----------|
| **Tester rapidement l'agent** | → Preview in Copilot (Option 1) |
| **Tester les Adaptive Cards** | → Teams Desktop (Option 2) |
| **Playground standalone** | → Convertir en SDK Agent (Option 3) - Non recommandé |

---

## 🚀 Quick Start : Preview in Copilot

```powershell
# 1. Provision (une seule fois)
# Dans Teams Toolkit, cliquez sur "Provision"

# 2. Lancer le backend
cd backend
py -m uvicorn main:app --port 3001

# 3. Dans VS Code :
# - Menu Run and Debug (F5)
# - Sélectionnez "Preview in Copilot (Chrome)"
# - Appuyez sur F5
```

---

## ❓ FAQ

**Q: Pourquoi je ne peux pas utiliser `agentsplayground` directement ?**
R: `agentsplayground` est conçu pour les SDK Agents (Bot Framework), pas pour les agents déclaratifs. Les agents déclaratifs utilisent une architecture différente.

**Q: Preview in Copilot = Playground ?**
R: Oui, c'est l'équivalent du Playground pour les agents déclaratifs. C'est l'environnement de test officiel.

**Q: Comment tester les Adaptive Cards alors ?**
R: Il faut utiliser Teams Desktop (Option 2) car les Adaptive Cards avec boutons sont spécifiques à Teams.

**Q: Puis-je avoir les deux (Playground + Adaptive Cards) ?**
R: Non, pas directement. Vous pouvez :
- Tester la logique dans Copilot (Preview)
- Tester les Adaptive Cards dans Teams Desktop

---

## 📚 Documentation

- [Microsoft 365 Agents Toolkit - Testing](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project)
- [Declarative Agents Overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/declarative-agents-overview)

