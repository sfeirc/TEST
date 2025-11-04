# 🎮 Compatibilité des Agents avec Teams Playground

## 📋 Types d'Agents et leur Compatibilité

Il existe **2 types d'agents** dans Microsoft 365 Agents Toolkit, chacun avec son propre outil de test :

---

## 1. SDK Agents (Bot Framework) ✅ Compatible avec Teams Playground

**Type :** SDK Agents (Bot Framework SDK)

**Caractéristiques :**
- ✅ **Compatible avec `agentsplayground` CLI** (Teams Playground standalone)
- Code écrit en Bot Framework SDK (C#, JavaScript, Python)
- Architecture basée sur des messages HTTP
- Endpoint standard : `/api/messages`

**Comment tester :**
```powershell
# Installer l'outil
npm install -g @microsoft/m365agentstoolkit-cli

# Lancer le Playground
agentsplayground -e "http://localhost:3978/api/messages"
```

**Structure du projet :**
```
project/
├── src/           # Code Bot Framework (C#/JS/Python)
├── bot.ts         # Logique du bot
└── index.ts       # Point d'entrée
```

**Avantages :**
- ✅ Contrôle total sur la logique
- ✅ Playground standalone disponible
- ✅ Test local sans Teams
- ✅ Débogage avancé possible

**Limitations :**
- ❌ Plus complexe à développer
- ❌ Nécessite du code Bot Framework
- ❌ Plus de maintenance

---

## 2. Declarative Agents ❌ PAS compatible avec Teams Playground

**Type :** Declarative Agents (Copilot Agents)

**Caractéristiques :**
- ❌ **NON compatible avec `agentsplayground` CLI**
- Configuration via JSON (pas de code)
- Utilise `declarativeAgent.json`
- Architecture basée sur Copilot

**Comment tester :**
- ✅ **"Preview in Copilot"** (équivalent du Playground)
  - Dans VS Code : Run and Debug → "Preview in Copilot (Chrome)"
- ✅ **Teams Desktop** (pour Adaptive Cards)
  - Upload custom app dans Teams

**Structure du projet :**
```
project/
├── appPackage/
│   ├── declarativeAgent.json  # Configuration de l'agent
│   ├── ai-plugin.json         # Actions/Plugins
│   └── manifest.json          # Manifest Teams
└── backend/                   # API backend
```

**Avantages :**
- ✅ Développement rapide (pas de code)
- ✅ Configuration simple (JSON)
- ✅ Intégration native Copilot
- ✅ Adaptive Cards supportées

**Limitations :**
- ❌ Pas de Playground standalone (`agentsplayground`)
- ❌ Moins de contrôle sur la logique
- ❌ Nécessite Copilot activé pour Teams Desktop

---

## 🔄 Tableau Comparatif

| Caractéristique | SDK Agents | Declarative Agents |
|----------------|------------|-------------------|
| **Teams Playground (`agentsplayground`)** | ✅ Oui | ❌ Non |
| **Preview in Copilot** | ❌ Non | ✅ Oui |
| **Teams Desktop** | ✅ Oui | ✅ Oui (si Copilot activé) |
| **Code requis** | ✅ Oui (Bot Framework) | ❌ Non (JSON seulement) |
| **Complexité** | 🔴 Élevée | 🟢 Faible |
| **Contrôle** | 🟢 Total | 🟡 Limitée |
| **Adaptive Cards** | ✅ Oui | ✅ Oui |
| **Débogage** | 🟢 Avancé | 🟡 Basique |

---

## 🎯 Votre Situation Actuelle

**Votre projet utilise : Declarative Agents**

D'après votre structure :
- ✅ `declarativeAgent.json` présent
- ✅ `ai-plugin.json` pour les actions
- ✅ Configuration JSON (pas de code Bot Framework)

**Donc :**
- ❌ **Vous NE POUVEZ PAS utiliser `agentsplayground` CLI**
- ✅ **Vous DEVEZ utiliser "Preview in Copilot"** (équivalent)

---

## 📝 Comment Identifier le Type d'Agent

### SDK Agent
- A un dossier `src/` avec du code (`.ts`, `.js`, `.cs`, `.py`)
- A un fichier `bot.ts` ou équivalent
- Utilise Bot Framework SDK
- Endpoint `/api/messages`

### Declarative Agent
- A un fichier `declarativeAgent.json`
- Pas de code Bot Framework
- Configuration uniquement en JSON
- Utilise `copilotAgents` dans `manifest.json`

---

## 🚀 Solutions pour Tester votre Agent Déclaratif

### Option 1 : Preview in Copilot ⭐ RECOMMANDÉ

**C'est l'équivalent du Playground pour les agents déclaratifs.**

1. Dans VS Code : Run and Debug (F5)
2. Sélectionnez "Preview in Copilot (Chrome)"
3. Appuyez sur F5

**Avantages :**
- ✅ Pas besoin de Copilot activé dans Teams
- ✅ Fonctionne immédiatement
- ✅ Test rapide de la logique

### Option 2 : Teams Desktop

**Pour tester les Adaptive Cards avec boutons.**

1. Backend accessible publiquement (cloudflared/Azure)
2. Mettre à jour OpenAPI avec URL publique
3. Rebuild ZIP
4. Upload dans Teams Desktop

### Option 3 : Convertir en SDK Agent

**Si vous voulez vraiment utiliser `agentsplayground` :**

⚠️ **Attention :** Cela nécessite de réécrire complètement votre agent en Bot Framework SDK.

**Étapes :**
1. Créer un nouveau projet SDK Agent
2. Migrer la logique vers Bot Framework
3. Implémenter les Adaptive Cards dans le code
4. Utiliser `agentsplayground` pour tester

**⚠️ Non recommandé** si vous avez déjà un agent déclaratif fonctionnel.

---

## ❓ FAQ

**Q: Pourquoi mon agent déclaratif ne fonctionne pas avec `agentsplayground` ?**
R: `agentsplayground` est conçu uniquement pour les SDK Agents (Bot Framework). Les agents déclaratifs utilisent une architecture différente basée sur Copilot.

**Q: Preview in Copilot = Teams Playground ?**
R: Oui, c'est l'équivalent du Playground pour les agents déclaratifs. C'est l'environnement de test officiel.

**Q: Puis-je convertir mon agent déclaratif en SDK Agent ?**
R: Oui, mais c'est un gros travail. Il faut réécrire toute la logique en Bot Framework SDK.

**Q: Quel type d'agent choisir ?**
R: 
- **Declarative Agent** : Si vous voulez développer rapidement sans code
- **SDK Agent** : Si vous avez besoin de contrôle total et de logique complexe

---

## 📚 Documentation

- [Microsoft 365 Agents Toolkit - Types d'Agents](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/)
- [SDK Agents Overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/sdk-agents-overview)
- [Declarative Agents Overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/declarative-agents-overview)
- [Testing with Teams Playground](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project)

