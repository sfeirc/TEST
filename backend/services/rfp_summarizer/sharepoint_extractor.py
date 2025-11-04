"""
Service d'extraction de texte depuis SharePoint
Extrait le texte depuis des liens de documents SharePoint
"""
import os
import re
import tempfile
from typing import Optional
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from .file_extractor import extract_text_from_file

def is_sharepoint_url(text: str) -> bool:
    """
    Vérifier si le texte est une URL SharePoint
    
    Args:
        text: Texte à vérifier
    
    Returns:
        True si c'est une URL SharePoint, False sinon
    """
    if not text:
        return False
    
    sharepoint_patterns = [
        r'https?://[^/]*\.sharepoint\.com',
        r'https?://sharepoint\.',
    ]
    
    for pattern in sharepoint_patterns:
        if re.search(pattern, text.strip(), re.IGNORECASE):
            return True
    
    return False

def extract_text_from_sharepoint(sharepoint_url: str) -> str:
    """
    Extraire le texte d'un document SharePoint
    
    Supporte:
    - Liens directs vers fichiers
    - Liens de bibliothèques de documents
    
    Requiert les variables d'environnement:
    - SHAREPOINT_CLIENT_ID
    - SHAREPOINT_CLIENT_SECRET
    - SHAREPOINT_TENANT_ID (ou URL du site)
    """
    
    # Récupérer les identifiants depuis l'environnement
    client_id = os.getenv("SHAREPOINT_CLIENT_ID")
    client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
    tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
    
    if not all([client_id, client_secret]):
        raise Exception(
            "Identifiants SharePoint non configurés. "
            "Veuillez définir SHAREPOINT_CLIENT_ID et SHAREPOINT_CLIENT_SECRET dans le fichier .env. "
            "Pour l'instant, veuillez télécharger le fichier et l'uploader directement."
        )
    
    try:
        # Parser l'URL SharePoint pour obtenir le site et le chemin du fichier
        site_url, file_server_relative_url = parse_sharepoint_url(sharepoint_url)
        
        if not site_url or not file_server_relative_url:
            raise Exception("Impossible de parser l'URL SharePoint. Veuillez vous assurer qu'il s'agit d'un lien valide vers un document SharePoint.")
        
        # S'authentifier avec SharePoint
        credentials = ClientCredential(client_id, client_secret)
        ctx = ClientContext(site_url).with_credentials(credentials)
        
        # Télécharger le fichier
        file = ctx.web.get_file_by_server_relative_url(file_server_relative_url)
        
        # Obtenir le nom du fichier
        file.get().execute_query()
        filename = file.properties.get("Name", "document.pdf")
        
        # Télécharger vers un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Télécharger le contenu du fichier
            with open(tmp_path, "wb") as local_file:
                file.download(local_file).execute_query()
            
            # Extraire le texte
            text = extract_text_from_file(tmp_path, filename)
            return text
            
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        raise Exception(f"Erreur lors de l'accès à SharePoint: {str(e)}")

def parse_sharepoint_url(url: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parser l'URL SharePoint pour extraire l'URL du site et le chemin du fichier
    
    Exemple d'entrée:
    https://contoso.sharepoint.com/sites/MySite/Shared%20Documents/RFP.pdf
    
    Retourne:
    ('https://contoso.sharepoint.com/sites/MySite', '/sites/MySite/Shared Documents/RFP.pdf')
    """
    try:
        # Extraire l'URL de base du site SharePoint
        match = re.match(r'(https?://[^/]+(?:/sites/[^/]+)?)', url)
        if not match:
            return None, None
        
        site_url = match.group(1)
        
        # Extraire l'URL relative au serveur (tout après l'URL du site)
        server_relative_url = url.replace(site_url, '')
        
        # Décodage URL
        from urllib.parse import unquote
        server_relative_url = unquote(server_relative_url)
        
        return site_url, server_relative_url
    
    except Exception as e:
        print(f"Erreur lors du parsing de l'URL SharePoint: {str(e)}")
        return None, None
