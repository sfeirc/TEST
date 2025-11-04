# 🔧 Résoudre "Installez Copilot pour pouvoir utiliser cette application"

## 🔍 Problème

Votre application utilise un **Agent Déclaratif** (Copilot Agent), qui nécessite que **Microsoft Copilot** soit activé dans votre environnement Teams.

---

## ✅ Solutions

### Option 1 : Activer Copilot dans Teams (Recommandé pour Production)

**Pour activer Copilot dans votre organisation Teams :**

1. **Demander à votre administrateur IT** d'activer Copilot pour votre tenant
   - Copilot nécessite une licence Microsoft 365 Copilot
   - L'admin doit activer la fonctionnalité dans le Centre d'administration Microsoft 365

2. **OU utiliser un compte avec Copilot déjà activé**
   - Si vous avez un compte de test avec Copilot (ex: `Agent_Presales@3fw0f6.onmicrosoft.com`)
   - Connectez-vous avec ce compte dans Teams Desktop

**Avantages :**
- ✅ Fonctionne directement dans Teams Desktop
- ✅ Tous les utilisateurs peuvent utiliser l'agent
- ✅ Solution permanente

**Limitation :**
- ⚠️ Nécessite une licence Copilot (coût supplémentaire)

---

### Option 2 : Utiliser "Preview in Copilot" (Pour Tests Rapides) ⭐ RECOMMANDÉ POUR DÉVELOPPEMENT

**C'est la solution la plus simple pour tester sans avoir besoin de Copilot activé dans Teams.**

#### Étapes :

1. **Dans VS Code, ouvrez le menu Run and Debug** (icône de lecture ou F5)

2. **Sélectionnez une des options :**
   - `Preview in Copilot (Chrome)`
   - `Preview in Copilot (Edge)`

3. **Appuyez sur F5** ou cliquez sur le bouton Play

4. **Une fenêtre Copilot s'ouvrira** dans votre navigateur

5. **Votre agent sera disponible** dans cette interface Copilot

**Avantages :**
- ✅ Pas besoin de Copilot activé dans Teams
- ✅ Pas besoin d'upload custom app
- ✅ Fonctionne immédiatement après Provision
- ✅ Parfait pour tester la logique de l'agent

**Limitations :**
- ❌ Les Adaptive Cards avec boutons ne fonctionnent pas (elles sont pour Teams uniquement)
- ❌ Ce n'est pas l'environnement Teams réel

---

### Option 3 : Utiliser Teams Desktop avec un compte Admin/Test

Si vous avez accès à un compte admin ou un compte de test avec les permissions nécessaires :

1. **Connectez-vous à Teams Desktop** avec ce compte
2. **Vérifiez que Copilot est disponible** (icône Copilot dans la barre latérale)
3. **Si Copilot n'apparaît pas**, contactez votre admin IT pour activer Copilot

---

### Option 4 : Vérifier les Permissions de l'Application

Parfois le problème vient des permissions. Vérifiez dans le Developer Portal :

1. Allez sur https://dev.teams.microsoft.com
2. Sélectionnez votre app "INFOTELdev"
3. **Configure → Permissions**
4. Assurez-vous que les permissions suivantes sont présentes :
   - `identity` (déjà présent)
   - `messageTeamMembers` (déjà présent)
   - Si nécessaire, ajoutez d'autres permissions selon vos besoins

---

## 🎯 Recommandation selon votre Situation

| Situation | Solution |
|-----------|----------|
| **Développement/Test rapide** | → Option 2 : Preview in Copilot |
| **Production dans l'entreprise** | → Option 1 : Demander activation Copilot à l'IT |
| **Test avec Adaptive Cards** | → Option 1 : Activer Copilot dans Teams Desktop |
| **Compte admin disponible** | → Option 3 : Utiliser compte admin |

---

## 🚀 Quick Start : Preview in Copilot

```powershell
# 1. Assurez-vous que le backend est démarré
cd backend
py -m uvicorn main:app --port 3001

# 2. Dans VS Code :
# - Ouvrez Run and Debug (F5)
# - Sélectionnez "Preview in Copilot (Chrome)"
# - Appuyez sur F5
```

---

## 📋 Checklist

- [ ] Backend démarré et accessible (localhost:3001 ou URL publique)
- [ ] Provision effectué dans Teams Toolkit
- [ ] Fichiers OpenAPI mis à jour avec la bonne URL
- [ ] Si Teams Desktop : Copilot activé OU compte admin utilisé
- [ ] Si Preview : Configuré dans VS Code Run and Debug

---

## ❓ FAQ

**Q: Pourquoi mon app nécessite Copilot ?**
R: Votre application utilise `copilotAgents` avec `declarativeAgents` dans le manifest. C'est une fonctionnalité Copilot spécifique.

**Q: Puis-je créer une app sans Copilot ?**
R: Oui, mais vous perdriez les fonctionnalités d'agent déclaratif. Vous devriez convertir en Bot Framework SDK, ce qui est beaucoup plus complexe.

**Q: Preview in Copilot = Teams Desktop ?**
R: Non, c'est un environnement de test séparé. Pour tester dans Teams Desktop réel, il faut Copilot activé.

**Q: Comment savoir si Copilot est activé dans mon tenant ?**
R: Vous devriez voir l'icône Copilot dans la barre latérale de Teams. Si elle n'apparaît pas, Copilot n'est pas activé pour votre compte.

---

## 📚 Documentation

- [Microsoft 365 Copilot - Activation](https://learn.microsoft.com/en-us/microsoft-365/copilot/requirements)
- [Teams Toolkit - Preview in Copilot](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project)

