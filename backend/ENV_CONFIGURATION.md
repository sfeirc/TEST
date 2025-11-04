# Configuration des Variables d'Environnement

## Fichier `.env`

Créer un fichier `.env` dans le répertoire `backend/` avec votre configuration:

### Configuration Globale du Modèle

```env
MODEL=gpt-5
```

Ce paramètre contrôle le modèle utilisé dans tous les services du projet. Changez-le une seule fois pour affecter tous les appels IA.

### Option 1: Azure OpenAI (Recommandé pour entreprise)

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-5
```

### Option 2: OpenAI Direct

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### Configuration SharePoint (Optionnel)

```env
SHAREPOINT_CLIENT_ID=your-app-client-id
SHAREPOINT_CLIENT_SECRET=your-app-secret
SHAREPOINT_TENANT_ID=your-tenant-id
```

## Obtenir les clés API

### Azure OpenAI
1. Aller sur le portail Azure: https://portal.azure.com
2. Créer une ressource "Azure OpenAI"
3. Déployer un modèle (gpt-5 recommandé)
4. Récupérer: Endpoint, Key, Deployment name

### OpenAI Direct
1. Aller sur https://platform.openai.com
2. Créer un compte et une clé API
3. Copier la clé `sk-...`

## Test de la configuration

```bash
cd backend
py -m uvicorn main:app --reload --port 3001
```

Puis ouvrir: http://localhost:3001/

Vous devriez voir:
```json
{
  "message": "API Infotel AI Agent",
  "version": "1.0.0",
  "status": {
    "summarizeRfp": "✅ Opérationnel",
    "generateDiagramFromText": "✅ Opérationnel",
    "generateDeckFromText": "✅ Opérationnel"
  }
}
```

