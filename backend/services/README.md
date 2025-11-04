# 📁 Structure des Services - Agents Infotel

## Organisation

Les services sont organisés par agent/fonctionnalité:

```
services/
├── common/                      # 🔧 Modules partagés
│   ├── extract_infotel_colors.py   # Charte graphique Infotel (couleurs PANTONE, polices)
│   └── __init__.py
│
├── rfp_summarizer/             # 📄 Agent: RFP Summarizer
│   ├── ai_summarizer.py           # IA pour analyse RFP
│   ├── file_extractor.py          # Extraction PDF/DOCX/TXT
│   ├── sharepoint_extractor.py    # Extraction depuis SharePoint
│   └── __init__.py
│
├── diagram_generator/          # 🎨 Agent: Diagram Generator
│   ├── diagram_generator.py       # IA pour spécification de diagrammes
│   ├── pptx_diagram_builder.py    # Création PowerPoint de diagrammes
│   └── __init__.py
│
├── deck_generator/             # 📊 Agent: Deck Generator
│   ├── deck_generator.py          # IA pour plan de présentation (skywork.ai level)
│   ├── infotel_template_builder.py # Builder PowerPoint PRODUCTION (template exact)
│   ├── pptx_deck_builder.py       # Builder PowerPoint BACKUP (compatibilité)
│   └── __init__.py
│
└── proposal_harmonizer/        # ✨ Agent: Proposal Harmonizer
    └── __init__.py                 # (À implémenter)
```

## 🎯 Agents Disponibles

### 1. RFP Summarizer (`/summarizeRfp`)
**Objectif**: Analyser et résumer les appels d'offres (RFP)

**Modules**:
- `ai_summarizer.py`: Utilise GPT-5 avec un prompt structuré de 200+ lignes pour analyser les RFP
- `file_extractor.py`: Extrait le texte de PDF, DOCX, TXT
- `sharepoint_extractor.py`: Récupère les documents depuis SharePoint

**Commandes**: `/summarize`, `/rfp`, `1`

**Entrée**: Fichier (PDF/DOCX), lien SharePoint, ou texte

**Sortie**: Analyse détaillée avec sections, lots, calendrier, budget, critères, etc.

---

### 2. Diagram Generator (`/generateDiagramFromText`)
**Objectif**: Créer des diagrammes/schémas techniques PowerPoint

**Modules**:
- `diagram_generator.py`: IA génère la spécification du diagramme
- `pptx_diagram_builder.py`: Crée le fichier PowerPoint avec python-pptx

**Commandes**: `/diagram`, `/schema`, `3`

**Entrée**: Description textuelle ou fichier technique

**Sortie**: Fichier PowerPoint (.pptx) téléchargeable et éditable

---

### 3. Deck Generator (`/generateDeckFromText`)
**Objectif**: Générer des présentations PowerPoint complètes (niveau skywork.ai)

**Modules**:
- `deck_generator.py`: IA avec prompt skywork.ai (124 lignes de règles)
  - Analyse intelligente du contenu
  - Architecture narrative professionnelle
  - Rédaction orientée bénéfice
  - Optimisations automatiques
  
- `infotel_template_builder.py`: **PRODUCTION** - Reproduction exacte du template Infotel
  - Couleurs PANTONE exactes (653C, 285C, 645C, 654C)
  - Police Segoe UI (Regular, Semilight, Semibold)
  - Logo Infotel officiel (PNG)
  - Pas de barre rose
  
- `pptx_deck_builder.py`: **BACKUP** - Builder alternatif

**Commandes**: `/deck`, `/presentation`, `2`

**Entrée**: Texte, fichier, ou lien SharePoint

**Sortie**: Présentation PowerPoint complète prête à présenter

---

### 4. Proposal Harmonizer (`/uniformizeProposal`)
**Objectif**: Standardiser les présentations selon la charte Infotel

**Status**: ⏳ À implémenter

**Commandes**: `/harmonize`, `/standardize`, `4`

---

## 🔧 Module Commun

### `common/extract_infotel_colors.py`
**Rôle**: SOURCE UNIQUE DE VÉRITÉ pour la charte graphique Infotel

**Contenu**:
- Couleurs PANTONE officielles avec RGB exact
- Polices Segoe UI (variantes)
- Référence CMYK pour impression

**Utilisé par**:
- ✅ `deck_generator/infotel_template_builder.py`
- ✅ `deck_generator/pptx_deck_builder.py`
- ✅ `diagram_generator/pptx_diagram_builder.py` (peut l'utiliser)

**Avantage**: Une seule modification met à jour tous les agents

---

## 📦 Imports

### Dans `main.py`
```python
# RFP Summarizer
from services.rfp_summarizer import (
    extract_text_from_file,
    extract_text_from_sharepoint,
    summarize_rfp_with_ai,
    is_sharepoint_url
)

# Diagram Generator
from services.diagram_generator import (
    generate_diagram_spec_with_ai,
    create_powerpoint_diagram
)

# Deck Generator
from services.deck_generator import (
    generate_deck_plan_with_ai,
    create_powerpoint_from_template  # Production
)
```

### Dans les services
```python
# Importer la charte graphique (depuis n'importe quel service)
from services.common import extract_colors_from_template, get_infotel_fonts

# Importer depuis le même package
from .file_extractor import extract_text_from_file  # Import relatif
```

---

## 🚀 Ajouter un Nouvel Agent

1. **Créer le dossier**:
   ```bash
   mkdir backend/services/mon_agent
   ```

2. **Créer les fichiers**:
   ```bash
   # Module IA
   touch backend/services/mon_agent/mon_agent_ai.py
   
   # Module Builder
   touch backend/services/mon_agent/mon_agent_builder.py
   
   # Init
   touch backend/services/mon_agent/__init__.py
   ```

3. **Configurer `__init__.py`**:
   ```python
   """
   Agent Mon Agent
   Description de ce que fait l'agent
   """
   from .mon_agent_ai import generer_avec_ai
   from .mon_agent_builder import creer_resultat
   
   __all__ = ['generer_avec_ai', 'creer_resultat']
   ```

4. **Importer la charte Infotel** (si besoin):
   ```python
   from services.common import extract_colors_from_template, get_infotel_fonts
   ```

5. **Utiliser dans `main.py`**:
   ```python
   from services.mon_agent import generer_avec_ai, creer_resultat
   ```

---

## ✅ Avantages de cette Structure

### 🎯 Clarté
- Chaque agent a son propre dossier
- Facile de trouver le code d'un agent spécifique
- Séparation claire des responsabilités

### 🔧 Maintenabilité
- Modifications isolées par agent
- Pas de risque de casser un autre agent
- Charte graphique centralisée

### 📈 Scalabilité
- Ajouter un agent = ajouter un dossier
- Pas de fichiers énormes
- Code modulaire et réutilisable

### 👥 Collaboration
- Plusieurs dev peuvent travailler sur différents agents
- Moins de conflits Git
- Revues de code plus faciles

---

## 📚 Références

- **Charte Infotel 2025**: `common/extract_infotel_colors.py`
- **Prompt skywork.ai**: `deck_generator/deck_generator.py` (lignes 10-124)
- **Template exact Infotel**: `deck_generator/infotel_template_builder.py`
- **API Configuration**: `../ENV_CONFIGURATION.md`
- **Architecture globale**: `../../ARCHITECTURE.md`

---

**Dernière mise à jour**: 28 octobre 2025  
**Structure**: Organisée par agent  
**Qualité**: Production-ready 🚀

