# 🤖 INFOTEL AI AGENT — Guide Complet (FR)

**Assistant IA pour Microsoft Teams**: analyse d'AO (RFP), génération de présentations PowerPoint éditables, création de diagrammes d’architecture, et harmonisation de slides selon la charte Infotel 2025.

---

## 🚀 Démarrage Rapide

### 1) Installation

```bash
cd backend
py -m pip install -r requirements.txt
py -m playwright install chromium --with-deps --no-shell
```

### 2) Configuration (.env)
Créez `backend/.env` et renseignez au minimum un des blocs suivants.

```env
# Modèle IA global pour TOUT le projet
MODEL=gpt-5

# Option 1: Azure OpenAI (recommandé)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-5

# Option 2: OpenAI direct
# OPENAI_API_KEY=sk-your-openai-key
```

Optionnel (SharePoint): consultez `backend/ENV_CONFIGURATION.md`.

### 3) Lancer en local
```bash
# Démarrer l’API
cd backend
py -m uvicorn main:app --reload --port 3001
```
Dans VS Code (Teams Toolkit): F5 pour lancer l’agent déclaratif dans Teams.

---

## 🧩 Architecture

- `appPackage/` — Agent déclaratif (instructions, Adaptive Cards, plugins OpenAPI)
- `backend/` — API FastAPI (RFP, Deck, Diagram, Harmonizer)
  - `services/*` — logique de traitement (IA, parsing, génération PPTX)
  - `generated_files/` — fichiers temporaires générés (HTML/PPTX)

Flux haut-niveau:
1) L’utilisateur envoie un fichier/lien/texte dans Teams
2) Adaptive Card propose l’action (analysée par règles + IA)
3) L’agent appelle le backend (FastAPI) pour exécuter l’action
4) Le backend renvoie liens, fichiers et résumés structurés

---

## 🛠️ Endpoints principaux (FastAPI)

- `POST /summarizeRfp` — Analyse d’un RFP (fichier, lien SharePoint, texte)
- `POST /generateDeckFromText` — Génère un plan + HTML + PPTX éditable
- `POST /generateDiagramFromText` — Génère un JSON de diagramme + PPTX
- `POST /uniformizeProposal` — Harmonise un .pptx existant (charte Infotel)
- `GET /health` — Statut rapide

Swagger: `http://localhost:3001/docs`

---

## 📚 Cas d’usage (Users Stories)

- Upload d’un fichier inconnu → suggestion d’action (RFP / Deck / Diagram / Harmonize)
- Demande texte: « crée une présentation … » → plan, preview HTML, puis PPTX éditable
- Fichier .pptx → harmonisation automatique (polices, couleurs, logo, structure)
- Contenu technique → proposition de diagramme (types: process, architecture, timeline…)
- Modification naturelle: « supprime la slide 3 », « ajoute une slide ROI » → application smart

---

## 🧪 Entrées supportées

- Fichiers: PDF, DOCX, PPTX, TXT, MD
- Liens SharePoint (optionnel, voir ENV)
- Texte libre

---

## 🧱 Hébergement (obligatoire)

- Microsoft héberge l’agent déclaratif Teams, **pas** votre backend
- Vous devez héberger `backend/` (Azure App Service, Container Apps, VM, etc.)
- L’URL publique du backend doit correspondre aux `servers` des fichiers OpenAPI dans `appPackage/apiSpecificationFile/`

---

## 🧼 Nettoyage & Structure de dépôt

- Dossiers supprimables du dépôt: caches Python (`__pycache__/`, `*.pyc`)
- À conserver: `backend/generated_files/` (utilisé au runtime; vide en git)
- Builds Teams (`appPackage/build/`) sont générés — ne pas éditer à la main

Exemple `.gitignore` (racine):
```
__pycache__/
*.pyc
appPackage/build/
backend/generated_files/*
!backend/generated_files/.gitkeep
```

---

## ⚙️ Variables d’environnement (rappel)

Voir `backend/ENV_CONFIGURATION.md`. Le paramètre global `MODEL` s’applique à tous les services. Si Azure OpenAI est configuré, `AZURE_OPENAI_DEPLOYMENT` a priorité côté Azure; sinon, OpenAI utilisera `MODEL`.

---

## ❓Dépannage rapide

- 401/403 IA: vérifiez clés et déploiements (Azure) ou `OPENAI_API_KEY`
- PPTX vide: contrôlez les logs FastAPI et la taille du contenu source
- Adaptive Cards vides: ne modifiez pas `appPackage/build/*`, éditez les sources dans `appPackage/`

---

**Version**: 2.0 (Approche HTML/CSS, prompts FR/EN)  
**Statut**: ✅ Prêt pour déploiement  
**Backend**: `backend/main.py` (FastAPI)
