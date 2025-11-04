# 🎴 Adaptive Cards avec Teams Playground

## ✅ Réponse Rapide

**Oui, avec Teams Playground (SDK Agent), vous pouvez utiliser des Adaptive Cards**, mais il y a des différences importantes par rapport aux Declarative Agents.

---

## 🎯 Adaptive Cards : SDK Agent vs Declarative Agent

### SDK Agent (Teams Playground)

**Création en CODE :**

```python
# bot.py - SDK Agent Python
from botbuilder.core import MessageFactory
from botbuilder.schema import Attachment

def create_welcome_card():
    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "Welcome!",
                "size": "Large"
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Click me",
                        "data": {"action": "click"}
                    }
                ]
            }
        ]
    }
    return MessageFactory.attachment(Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card
    ))

# Utilisation
await turn_context.send_activity(create_welcome_card())
```

**Avantages :**
- ✅ Création dynamique (génération conditionnelle)
- ✅ Logique complexe dans le code
- ✅ Test avec Teams Playground
- ✅ Contrôle total

**Limitations :**
- ❌ Plus complexe à créer (code au lieu de JSON)
- ❌ Nécessite Bot Framework SDK
- ⚠️ Teams Playground peut avoir des limitations selon les versions

---

### Declarative Agent (votre cas actuel)

**Création en JSON (statique) :**

```json
// appPackage/adaptiveCards/summarizeRfp.json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "body": [
    {
      "type": "TextBlock",
      "text": "RFP Analysis"
    }
  ]
}
```

**Avantages :**
- ✅ Configuration simple (JSON)
- ✅ Pas de code requis
- ✅ Facile à maintenir

**Limitations :**
- ❌ Statique (pas de génération dynamique)
- ❌ Preview in Copilot : boutons limités
- ✅ Teams Desktop : fonctionne complètement

---

## 🔍 Comparaison Détaillée

| Aspect | SDK Agent (Playground) | Declarative Agent |
|--------|----------------------|-------------------|
| **Création** | Code (Python/JS/C#) | JSON statique |
| **Dynamique** | ✅ Oui (conditionnel) | ❌ Non (statique) |
| **Teams Playground** | ✅ Supporté | ❌ Non compatible |
| **Preview in Copilot** | ❌ Non | ✅ Oui (limité) |
| **Teams Desktop** | ✅ Complet | ✅ Complet |
| **Boutons/Actions** | ✅ Complet | ✅ Complet (Teams Desktop) |
| **Complexité** | 🔴 Élevée | 🟢 Faible |

---

## 🎮 Teams Playground : Limitations Potentielles

**Teams Playground peut avoir des limitations :**

1. ⚠️ **Certaines actions peuvent ne pas fonctionner** (selon version)
2. ⚠️ **Rendu visuel peut différer** de Teams Desktop
3. ⚠️ **Interactions complexes** peuvent nécessiter Teams Desktop

**Pour un test complet des Adaptive Cards :**
- Teams Desktop reste la référence
- Teams Playground est bon pour la logique de base

---

## 💡 Recommandation selon votre Besoin

### Si vous voulez Teams Playground + Adaptive Cards

**Option : Convertir en SDK Agent**

1. Créer un SDK Agent Python
2. Coder les Adaptive Cards en Python
3. Tester avec `agentsplayground`
4. ⚠️ **Gros travail** : réécriture complète

**Exemple de code SDK Agent avec Adaptive Card :**

```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Attachment
from botbuilder.core import MessageFactory

class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        
        if "rfp" in user_message.lower():
            # Créer une Adaptive Card dynamique
            card = self.create_rfp_card(user_message)
            await turn_context.send_activity(card)
    
    def create_rfp_card(self, text: str):
        card_json = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "RFP Analysis",
                    "size": "Large",
                    "weight": "Bolder"
                },
                {
                    "type": "TextBlock",
                    "text": f"Analyzing: {text[:50]}...",
                    "wrap": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Analyze",
                    "data": {"action": "analyze", "text": text}
                }
            ]
        }
        
        return MessageFactory.attachment(Attachment(
            content_type="application/vnd.microsoft.card.adaptive",
            content=card_json
        ))
```

---

## 🎯 Votre Situation Actuelle

**Vous avez des Adaptive Cards en JSON** (Declarative Agent) :

- ✅ `appPackage/adaptiveCards/summarizeRfp.json`
- ✅ `appPackage/adaptiveCards/generateDeckFromText.json`
- ✅ `appPackage/adaptiveCards/generateDiagramFromText.json`
- ✅ `appPackage/adaptiveCards/uniformizeProposal.json`

**Pour tester ces cartes :**

### Option 1 : Teams Desktop (Recommandé) ⭐

**Fonctionne parfaitement avec vos Adaptive Cards JSON :**

1. Backend accessible (cloudflared/Azure)
2. Mettre à jour OpenAPI avec URL publique
3. Rebuild ZIP
4. Upload dans Teams Desktop
5. ✅ **Toutes vos Adaptive Cards fonctionnent**

### Option 2 : Preview in Copilot

**Limitations :**
- ❌ Boutons peuvent ne pas fonctionner
- ✅ Affichage visuel OK
- ⚠️ Pas de test complet

### Option 3 : Convertir en SDK Agent

**Pour Teams Playground :**
- ⚠️ Nécessite de réécrire les cartes en code
- ⚠️ Gros travail de migration
- ✅ Contrôle total + Teams Playground

---

## 📊 Tableau de Décision

| Besoin | Solution Recommandée |
|--------|---------------------|
| **Tester rapidement** | Preview in Copilot |
| **Tester Adaptive Cards complètement** | Teams Desktop ⭐ |
| **Teams Playground + Adaptive Cards** | Convertir en SDK Agent (beaucoup de travail) |
| **Développement rapide** | Rester Declarative Agent + Teams Desktop |

---

## 🚀 Conclusion

**Oui, Teams Playground supporte les Adaptive Cards**, mais :

1. ⚠️ **Il faut être un SDK Agent** (Bot Framework)
2. ⚠️ **Les cartes doivent être créées en code** (pas JSON statique)
3. ⚠️ **Teams Desktop reste meilleur** pour tester complètement

**Pour votre cas :**
- ✅ **Vos Adaptive Cards JSON fonctionnent parfaitement dans Teams Desktop**
- ✅ **Pas besoin de Teams Playground** - Teams Desktop est suffisant
- ❌ **Convertir en SDK Agent = beaucoup de travail** pour peu de bénéfice

**Recommandation : Restez avec Declarative Agent + Teams Desktop pour tester vos Adaptive Cards.**

---

## 📚 Documentation

- [Adaptive Cards avec Bot Framework](https://learn.microsoft.com/en-us/azure/bot-service/bot-builder-howto-add-media-attachments?view=azure-bot-service-4.0&tabs=python)
- [Teams Playground Limitations](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project)

