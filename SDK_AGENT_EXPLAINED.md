# 🤖 SDK Agents - Explication Complète

## 📋 Qu'est-ce qu'un SDK Agent ?

Un **SDK Agent** est un agent développé avec le **Bot Framework SDK** (Microsoft Bot Framework). C'est un type d'agent qui nécessite du **code de programmation** (C#, JavaScript, TypeScript, Python) contrairement aux Declarative Agents qui utilisent uniquement de la configuration JSON.

---

## 🔍 SDK Agent vs Declarative Agent

### SDK Agent (Bot Framework)
- ✅ **Code requis** : C#, JavaScript, TypeScript, Python
- ✅ **Bot Framework SDK** : Utilise les bibliothèques Microsoft Bot Framework
- ✅ **Contrôle total** : Logique métier personnalisée dans le code
- ✅ **Teams Playground** : Compatible avec `agentsplayground` CLI
- ❌ **Plus complexe** : Nécessite des compétences en développement

### Declarative Agent (votre cas actuel)
- ✅ **Configuration JSON uniquement** : Pas de code
- ✅ **Développement rapide** : Configuration simple
- ✅ **Preview in Copilot** : Test direct dans Copilot
- ❌ **Contrôle limité** : Logique basée sur les capacités déclaratives
- ❌ **Pas de Teams Playground** : Pas compatible avec `agentsplayground`

---

## 🏗️ Structure d'un Projet SDK Agent

Un projet SDK Agent ressemble à ceci :

```
sdk-agent-project/
├── src/
│   ├── bot.ts              # Logique principale du bot
│   ├── index.ts            # Point d'entrée (serveur)
│   ├── dialogs/            # Dialogs pour la conversation
│   │   └── mainDialog.ts
│   ├── cards/              # Adaptive Cards (code)
│   │   └── welcomeCard.ts
│   └── models/             # Modèles de données
│       └── userContext.ts
├── package.json            # Dépendances Node.js
├── tsconfig.json           # Configuration TypeScript
└── .env                    # Variables d'environnement
```

### Exemple de Code SDK Agent (TypeScript)

**bot.ts** - Logique principale :
```typescript
import { ActivityHandler, MessageFactory } from 'botbuilder';
import { TurnContext } from 'botbuilder-core';

export class MyBot extends ActivityHandler {
    constructor() {
        super();
        
        // Gestion des messages
        this.onMessage(async (context, next) => {
            const userMessage = context.activity.text;
            
            // Logique personnalisée
            if (userMessage.includes('hello')) {
                await context.sendActivity('Hello! How can I help you?');
            } else {
                await context.sendActivity('I received your message!');
            }
            
            await next();
        });
        
        // Gestion des membres qui rejoignent
        this.onMembersAdded(async (context, next) => {
            const welcomeCard = MessageFactory.attachment(
                createWelcomeCard()
            );
            await context.sendActivity(welcomeCard);
            await next();
        });
    }
}
```

**index.ts** - Serveur HTTP :
```typescript
import express from 'express';
import { BotFrameworkAdapter } from 'botbuilder';
import { MyBot } from './bot';

const adapter = new BotFrameworkAdapter({
    appId: process.env.MicrosoftAppId,
    appPassword: process.env.MicrosoftAppPassword
});

const bot = new MyBot();

const server = express();

server.post('/api/messages', (req, res) => {
    adapter.processActivity(req, res, async (context) => {
        await bot.run(context);
    });
});

server.listen(3978, () => {
    console.log('Bot server is running on port 3978');
});
```

---

## 🎯 Quand Utiliser un SDK Agent ?

### Utilisez SDK Agent si :
- ✅ Vous avez besoin de **logique métier complexe**
- ✅ Vous voulez un **contrôle total** sur le comportement
- ✅ Vous avez des **compétences en développement** (C#/JS/Python)
- ✅ Vous voulez utiliser **Teams Playground** (`agentsplayground`)
- ✅ Vous avez besoin de **débogage avancé**
- ✅ Vous voulez intégrer avec des **systèmes externes complexes**

### Utilisez Declarative Agent si :
- ✅ Vous voulez **développer rapidement** sans code
- ✅ Votre logique est **simple** (actions déclaratives)
- ✅ Vous préférez la **configuration JSON**
- ✅ Vous voulez utiliser **Preview in Copilot**
- ✅ Vous avez besoin d'**Adaptive Cards simples**

---

## 🚀 Comment Créer un SDK Agent

### Option 1 : Via Teams Toolkit (VS Code)

1. **Ouvrez Teams Toolkit** dans VS Code
2. **Créer un nouveau projet** (Ctrl+Shift+P → "Teams: Create New Project")
3. **Sélectionnez "Teams Agents and Apps"**
4. **Choisissez "Bot" ou "SDK Agent"**
5. **Sélectionnez le langage** : TypeScript, JavaScript, ou C#
6. **Sélectionnez les capacités** : Bot, Message Extension, etc.

### Option 2 : Via CLI

```powershell
# Installer Teams Toolkit CLI
npm install -g @microsoft/teamsfx-cli

# Créer un nouveau projet SDK Agent
teamsfx new --template bot --programming-language typescript
```

---

## 📊 Comparaison Détaillée

| Aspect | SDK Agent | Declarative Agent |
|-------|-----------|-------------------|
| **Type de développement** | Code (C#/JS/Python) | Configuration JSON |
| **Complexité** | 🔴 Élevée | 🟢 Faible |
| **Temps de développement** | 🔴 Plus long | 🟢 Rapide |
| **Contrôle** | 🟢 Total | 🟡 Limitée |
| **Teams Playground** | ✅ Oui (`agentsplayground`) | ❌ Non |
| **Preview in Copilot** | ❌ Non | ✅ Oui |
| **Débogage** | 🟢 Avancé (code) | 🟡 Basique (logs) |
| **Adaptive Cards** | ✅ Code/Création dynamique | ✅ JSON statique |
| **Intégrations externes** | 🟢 Facile (code) | 🟡 Via API/Plugins |
| **Compétences requises** | 🔴 Développement | 🟢 Configuration |

---

## 🔧 Exemple : SDK Agent avec Actions Personnalisées

Dans un SDK Agent, vous pouvez créer des actions complexes :

```typescript
// Action personnalisée pour analyser un RFP
class RfpAnalyzerAction {
    async execute(context: TurnContext, args: any) {
        // Logique complexe en code
        const rfpText = args.rfpText;
        
        // Appel API personnalisé
        const analysis = await this.callBackendAPI(rfpText);
        
        // Création dynamique d'Adaptive Card
        const card = this.createAnalysisCard(analysis);
        
        await context.sendActivity(MessageFactory.attachment(card));
    }
    
    private async callBackendAPI(text: string) {
        // Logique d'appel API complexe
        // ...
    }
    
    private createAnalysisCard(analysis: any) {
        // Création dynamique de carte
        // ...
    }
}
```

Dans un Declarative Agent, c'est fait via `ai-plugin.json` avec OpenAPI.

---

## 🎮 Tester un SDK Agent

### Avec Teams Playground

```powershell
# Installer l'outil
npm install -g @microsoft/m365agentstoolkit-cli

# Lancer le bot localement
npm start

# Dans un autre terminal, lancer le Playground
agentsplayground -e "http://localhost:3978/api/messages"
```

### Avec Teams Desktop

1. Déployer le bot sur Azure Bot Service
2. Configurer l'app dans Teams
3. Upload dans Teams Desktop

---

## 📚 Votre Situation

**Votre projet actuel : Declarative Agent**

- ✅ Utilise `declarativeAgent.json`
- ✅ Configuration JSON uniquement
- ✅ Pas de code Bot Framework
- ✅ Test via "Preview in Copilot"

**Si vous voulez convertir en SDK Agent :**

⚠️ **C'est un gros travail** :
1. Créer un nouveau projet SDK Agent
2. Réécrire toute la logique en Bot Framework
3. Migrer les actions vers du code
4. Implémenter les Adaptive Cards dans le code
5. Tester avec `agentsplayground`

**Recommandation :** Restez avec Declarative Agent sauf si vous avez vraiment besoin de logique complexe ou de Teams Playground.

---

## 📖 Documentation

- [Bot Framework SDK Documentation](https://learn.microsoft.com/en-us/azure/bot-service/)
- [Teams Toolkit - Create Bot](https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/create-new-project)
- [SDK Agents Overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/sdk-agents-overview)

---

## ❓ FAQ

**Q: Puis-je avoir les deux (SDK + Declarative) ?**
R: Non, ce sont deux architectures différentes. Choisissez l'un ou l'autre.

**Q: Quel est le meilleur choix ?**
R: 
- **Débutant/rapide** → Declarative Agent
- **Logique complexe/contrôle total** → SDK Agent

**Q: Puis-je migrer de Declarative à SDK ?**
R: Oui, mais c'est une réécriture complète. Non recommandé sauf si nécessaire.

**Q: SDK Agent peut-il utiliser Preview in Copilot ?**
R: Non, SDK Agents utilisent Teams Playground. Preview in Copilot est pour Declarative Agents.

