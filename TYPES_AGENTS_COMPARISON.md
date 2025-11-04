# 🎯 Types d'Agents dans Microsoft 365 Agents Toolkit - Comparaison Complète

## 📋 Les 4 Types d'Agents Disponibles

Quand vous créez un nouveau projet dans Teams Toolkit, vous avez plusieurs options. Voici les différences :

---

## 1. Declarative Agent (votre cas actuel)

**Description :** Agent configuré uniquement en JSON, sans code.

**Caractéristiques :**
- ✅ Configuration JSON uniquement (`declarativeAgent.json`)
- ✅ Développement rapide (pas de code)
- ✅ Actions définies via OpenAPI (`ai-plugin.json`)
- ✅ Adaptive Cards en JSON statique
- ✅ Preview in Copilot pour tester
- ❌ Pas compatible avec Teams Playground (`agentsplayground`)

**Quand l'utiliser :**
- Développement rapide
- Logique simple (actions déclaratives)
- Pas besoin de contrôle total

**Structure :**
```
project/
├── appPackage/
│   ├── declarativeAgent.json
│   ├── ai-plugin.json
│   └── manifest.json
└── backend/  (API REST séparée)
```

---

## 2. Custom Engine Agent ⚠️ Différent de SDK Agent Standard

**Description :** Agent avec votre propre moteur d'orchestration IA (LLM personnalisé).

**Caractéristiques :**
- ✅ **Votre propre moteur LLM** (Azure AI Foundry, Semantic Kernel, LangChain, OpenAI Agents, etc.)
- ✅ Contrôle total sur l'orchestration IA
- ✅ Code requis (C# ou JavaScript - **Python pas encore supporté**)
- ✅ Intégration avec des frameworks IA externes
- ✅ Compatible avec Teams Playground (`agentsplayground`)
- ❌ Plus complexe (gestion de l'orchestration)

**Quand l'utiliser :**
- Vous voulez utiliser un LLM spécifique (non Azure OpenAI)
- Vous voulez intégrer LangChain, Semantic Kernel, etc.
- Vous avez besoin d'orchestration IA personnalisée
- Vous voulez Teams Playground + contrôle total sur l'IA

**Structure :**
```
project/
├── src/
│   ├── bot.ts          # Bot Framework
│   ├── orchestrator.ts  # Votre moteur IA personnalisé
│   └── ai-engine/       # Intégration LangChain/Semantic Kernel/etc.
```

**Exemple :**
```typescript
// Utilise LangChain au lieu d'Azure OpenAI standard
import { LangChain } from 'langchain';

class CustomEngineAgent {
    private llm: LangChain;
    
    async process(message: string) {
        // Votre logique d'orchestration personnalisée
        return await this.llm.invoke(message);
    }
}
```

---

## 3. SDK Agent (Bot Framework Standard) - "Teams Agents and Apps" → "Bot"

**Description :** Agent Bot Framework standard avec Azure OpenAI.

**Caractéristiques :**
- ✅ Bot Framework SDK standard
- ✅ Azure OpenAI intégré (par défaut)
- ✅ Code requis (C#, JavaScript, TypeScript, Python)
- ✅ Compatible avec Teams Playground (`agentsplayground`)
- ✅ Gestion des conversations standard
- ❌ Utilise Azure OpenAI (pas votre propre LLM)

**Quand l'utiliser :**
- Vous voulez Teams Playground
- Vous utilisez Azure OpenAI (standard)
- Vous voulez un Bot Framework classique
- Vous n'avez pas besoin d'orchestration IA personnalisée

**Structure :**
```
project/
├── src/
│   ├── bot.ts          # Bot Framework standard
│   └── dialogs/         # Dialogs Teams
└── .env (Azure OpenAI)
```

---

## 4. Teams Agents and Apps (autres options)

**Description :** Options diverses pour Teams (Bot, Message Extension, Tab, etc.)

**Caractéristiques :**
- ✅ Différentes capacités Teams (Bot, Tab, Message Extension)
- ✅ Bot Framework SDK standard
- ✅ Compatible avec Teams Playground (si Bot)

---

## 🔄 Tableau Comparatif Complet

| Aspect | Declarative Agent | Custom Engine Agent | SDK Agent (Standard) |
|--------|------------------|---------------------|---------------------|
| **Configuration** | JSON uniquement | Code (C#/JS) | Code (C#/JS/Python) |
| **Moteur IA** | Azure OpenAI (via actions) | Votre choix (LangChain, Semantic Kernel, etc.) | Azure OpenAI (standard) |
| **Orchestration** | Déclarative | Personnalisée (vous) | Bot Framework standard |
| **Teams Playground** | ❌ Non | ✅ Oui | ✅ Oui |
| **Preview in Copilot** | ✅ Oui | ❌ Non | ❌ Non |
| **Complexité** | 🟢 Faible | 🔴 Élevée | 🟡 Moyenne |
| **Contrôle** | 🟡 Limitée | 🟢 Total | 🟢 Total |
| **Python** | ✅ (backend séparé) | ❌ Pas encore | ✅ Oui |
| **Adaptive Cards** | ✅ JSON statique | ✅ Code dynamique | ✅ Code dynamique |

---

## 🎯 Pour Teams Playground + Adaptive Cards

**Vous avez 2 options :**

### Option 1 : Custom Engine Agent
- ✅ Teams Playground compatible
- ✅ Votre propre moteur IA (LangChain, etc.)
- ✅ Contrôle total
- ❌ Plus complexe
- ❌ Python pas encore supporté (C#/JS seulement)

### Option 2 : SDK Agent Standard
- ✅ Teams Playground compatible
- ✅ Azure OpenAI standard
- ✅ Python supporté
- ✅ Plus simple que Custom Engine
- ❌ Moins de contrôle sur l'orchestration IA

---

## 💡 Réponse à votre Question

**"Donc dans le SDK c'est le : Custom Engine Agent"**

**Partiellement correct !**

- ✅ **Custom Engine Agent** = Type d'agent avec SDK qui permet Teams Playground
- ⚠️ **Mais** : Custom Engine Agent est plus spécifique (votre propre moteur IA)
- ✅ **SDK Agent standard** = Autre option qui permet aussi Teams Playground

**Pour Teams Playground + Adaptive Cards, vous pouvez choisir :**
1. **Custom Engine Agent** - Si vous voulez votre propre moteur IA (LangChain, etc.)
2. **SDK Agent Standard** - Si Azure OpenAI standard vous suffit

**Les deux sont compatibles avec Teams Playground !**

---

## 📊 Recommandation selon votre Besoin

| Besoin | Type d'Agent Recommandé |
|--------|------------------------|
| **Développement rapide** | Declarative Agent (votre cas actuel) |
| **Teams Playground + Adaptive Cards** | SDK Agent Standard ou Custom Engine Agent |
| **Votre propre LLM/Orchestration** | Custom Engine Agent |
| **Azure OpenAI standard** | SDK Agent Standard |
| **LangChain/Semantic Kernel** | Custom Engine Agent |

---

## 🚀 Conclusion

**Oui, Custom Engine Agent est un type de SDK Agent**, mais :

- **Custom Engine Agent** = SDK Agent avec votre propre moteur IA
- **SDK Agent Standard** = SDK Agent avec Azure OpenAI standard

**Les deux permettent Teams Playground + Adaptive Cards !**

**Pour votre cas :**
- Si vous voulez juste Teams Playground + Adaptive Cards → **SDK Agent Standard** suffit
- Si vous voulez LangChain/Semantic Kernel → **Custom Engine Agent**

---

## 📚 Documentation

- [Custom Engine Agents](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/create-deploy-agents-sdk)
- [SDK Agents Overview](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/sdk-agents-overview)
- [Teams Playground](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project)

