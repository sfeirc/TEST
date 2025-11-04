# Procédure d'hébergement - Agent IA Infotel

## 📋 Vue d'ensemble

Cette application est un **backend FastAPI Python** qui doit être hébergé de manière accessible publiquement pour permettre à l'agent Microsoft Teams de l'utiliser via des appels API HTTPS.

### Architecture

- **Backend API**: FastAPI (Python) - **À héberger**
- **Agent Teams**: Déclaratif Microsoft 365 - **Hébergé par Microsoft** (ne nécessite pas d'hébergement)

---

## 🛠️ Spécifications techniques

### Technologies

- **Framework**: FastAPI 0.109.0
- **Langage**: Python 3.11+ (recommandé 3.11.1)
- **Serveur**: Uvicorn avec support standard
- **Port**: 3001 (configurable via variable d'environnement)

### Dépendances Python

```

# FastAPI and server
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Document processing
PyPDF2==3.0.1
python-docx==1.1.0
chardet==5.2.0

# SharePoint integration
Office365-REST-Python-Client==2.5.3

# OpenAI / Azure OpenAI
openai==1.12.0

# PowerPoint generation for diagrams
python-pptx==0.6.23

# HTML/CSS parsing for HTML→PPTX conversion (skywork.ai approach)
beautifulsoup4==4.12.3
lxml==5.1.0

# Environment and utilities
python-dotenv==1.0.0
pydantic==2.5.3

```

### Structure de l'application

```
backend/
├── main.py                 # Point d'entrée FastAPI
├── services/               # Modules métier
│   ├── rfp_summarizer/     # Résumé d'appels d'offres
│   ├── deck_generator/     # Génération de présentations
│   ├── diagram_generator/  # Génération de diagrammes
│   └── proposal_harmonizer/ # Harmonisation de propositions
├── generated_files/        # Dossier de stockage des fichiers générés
├── requirements.txt        # Dépendances Python
└── .env                    # Variables d'environnement (à créer)
```

---

## 🔧 Configuration requise

### Variables d'environnement

Créer un fichier `.env` dans le dossier `backend/` avec les variables suivantes:

```env
# Server Configuration
PORT=3001

# Azure OpenAI Configuration
# AZURE_OPENAI_DEPLOYMENT est utilisé dans tous les services (Azure OpenAI)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_DEPLOYMENT=gpt-5

# OR OpenAI Configuration (Alternative)
# OPENAI_API_KEY=sk-your-openai-key

# SharePoint Configuration 
# SHAREPOINT_CLIENT_ID=your-app-client-id
# SHAREPOINT_CLIENT_SECRET=your-app-client-secret
# SHAREPOINT_TENANT_ID=your-tenant-id


```

