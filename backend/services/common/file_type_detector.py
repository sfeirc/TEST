"""
Détecteur intelligent de contenu universel
Suggère l'action la plus pertinente selon le contenu
Supporte: fichiers, liens SharePoint, texte direct
Utilise l'IA (GPT-5) pour une analyse avancée
"""
import re
from typing import Dict, Optional
from .ai_content_analyzer import analyze_content_with_ai, merge_ai_and_rule_based_detection

def detect_file_purpose(filename: str, content_preview: Optional[str] = None) -> Dict[str, str]:
    """
    Détecter le type et l'usage probable d'un fichier
    
    Args:
        filename: Nom du fichier
        content_preview: Aperçu du contenu (premières lignes)
    
    Returns:
        Dict avec:
        - suggested_action: L'action recommandée
        - suggestion_reason: Raison de la suggestion
        - filename: Nom du fichier
    """
    
    filename_lower = filename.lower()
    
    # Détection 1: Fichier PowerPoint → Harmoniser
    if filename_lower.endswith(('.pptx', '.ppt')):
        return {
            "suggested_action": "harmonize",
            "suggestion_reason": "💡 Ce fichier PowerPoint peut être harmonisé selon la charte Infotel 2025",
            "filename": filename
        }
    
    # Détection 2: Nom de fichier contient "RFP", "AO", "Appel d'offres", etc.
    rfp_keywords = [
        'rfp', 'appel', 'offre', 'ao', 'consultation', 'marche', 'marché',
        'tender', 'proposal', 'request for proposal', 'cahier', 'charges',
        'cctp', 'dce', 'reglement', 'règlement'
    ]
    
    if any(keyword in filename_lower for keyword in rfp_keywords):
        return {
            "suggested_action": "summarize",
            "suggestion_reason": "💡 Ce document semble être un appel d'offres (RFP). Je peux l'analyser pour vous.",
            "filename": filename
        }
    
    # Détection 3: Contenu suggère un RFP
    if content_preview:
        content_lower = content_preview.lower()
        
        # Mots-clés très spécifiques aux RFP
        rfp_content_keywords = [
            'marché public', "appel d'offres", 'date limite', 'critères de sélection',
            'budget annuel', 'lot n°', 'pénalités', 'clause', 'article',
            'soumissionnaire', 'candidat', 'offre', 'montant estimé',
            'procédure', 'règlement de consultation', "acte d'engagement"
        ]
        
        matches = sum(1 for keyword in rfp_content_keywords if keyword in content_lower)
        
        if matches >= 3:  # Si au moins 3 mots-clés RFP trouvés
            return {
                "suggested_action": "summarize",
                "suggestion_reason": f"💡 Le contenu contient {matches} indicateurs d'appel d'offres. Analyse recommandée.",
                "filename": filename
            }
        
        # Mots-clés suggérant un document technique → Diagramme
        technical_keywords = [
            'architecture', 'infrastructure', 'schéma', 'diagramme', 
            'serveur', 'réseau', 'cloud', 'aws', 'azure', 'microservice',
            'api', 'base de données', 'flux', 'composant', 'module'
        ]
        
        tech_matches = sum(1 for keyword in technical_keywords if keyword in content_lower)
        
        if tech_matches >= 3:
            return {
                "suggested_action": "diagram",
                "suggestion_reason": f"💡 Document technique détecté. Un diagramme d'architecture pourrait être utile.",
                "filename": filename
            }
    
    # Détection 4: Fichiers texte génériques → Présentation
    if filename_lower.endswith(('.pdf', '.docx', '.doc', '.txt', '.md')):
        return {
            "suggested_action": "deck",
            "suggestion_reason": "💡 Je peux transformer ce document en présentation PowerPoint professionnelle.",
            "filename": filename
        }
    
    # Fallback: Aucune suggestion spécifique
    return {
        "suggested_action": None,
        "suggestion_reason": "Choisissez l'action qui convient le mieux à votre besoin.",
        "filename": filename
    }

def get_content_preview(file_path: str, max_chars: int = 2000) -> str:
    """
    Obtenir un aperçu du contenu d'un fichier pour analyse
    
    Args:
        file_path: Chemin vers le fichier
        max_chars: Nombre maximum de caractères à lire
    
    Returns:
        Aperçu du contenu
    """
    try:
        from services.rfp_summarizer import extract_text_from_file
        import os
        
        filename = os.path.basename(file_path)
        full_text = extract_text_from_file(file_path, filename)
        
        # Retourner juste les premiers caractères
        return full_text[:max_chars] if full_text else ""
    
    except Exception as e:
        print(f"Erreur lors de l'aperçu du fichier: {str(e)}")
        return ""

async def detect_content_intent(
    text: Optional[str] = None,
    filename: Optional[str] = None,
    is_sharepoint_link: bool = False,
    content_preview: Optional[str] = None,
    use_ai: bool = True
) -> Dict[str, any]:
    """
    Détection intelligente universelle de l'intention utilisateur
    Fonctionne avec: texte direct, fichiers uploadés, liens SharePoint
    Utilise l'IA (GPT-5) pour une analyse avancée si disponible
    
    Args:
        text: Texte tapé par l'utilisateur (ou None)
        filename: Nom du fichier uploadé (ou None)
        is_sharepoint_link: True si c'est un lien SharePoint
        content_preview: Aperçu du contenu (si disponible)
        use_ai: Si True, utilise l'IA pour l'analyse (par défaut)
    
    Returns:
        {
            "input_type": "text" | "file" | "sharepoint",
            "suggested_action": "summarize" | "deck" | "diagram" | "harmonize" | None,
            "suggestion_reason": "Raison de la suggestion",
            "confidence": 0.0-1.0,  # Confiance dans la suggestion
            "alternative_actions": ["action2", "action3"],  # Actions alternatives
            "detection_method": "ai" | "rules" | "ai_moderate" | "rules_fallback",
            "ai_powered": True | False
        }
    """
    
    # Analyse du contenu disponible
    analysis_content = content_preview or text or ""
    
    # Déterminer le type d'input
    if is_sharepoint_link:
        input_type = "sharepoint"
        source_info = "lien SharePoint"
    elif filename:
        input_type = "file"
        source_info = f"fichier {filename}"
    else:
        input_type = "text"
        source_info = "texte direct"
    
    # Si c'est un fichier, utiliser la détection spécifique au fichier
    if filename:
        file_detection = detect_file_purpose(filename, content_preview)
        
        confidence = 0.9 if file_detection["suggested_action"] else 0.5
        
        return {
            "input_type": input_type,
            "suggested_action": file_detection.get("suggested_action"),
            "suggestion_reason": file_detection.get("suggestion_reason"),
            "confidence": confidence,
            "alternative_actions": _get_alternative_actions(file_detection.get("suggested_action")),
            "source_info": source_info
        }
    
    # Analyse du texte direct ou contenu SharePoint
    if analysis_content:
        content_lower = analysis_content.lower()
        
        # Détection 1: RFP / Appel d'offres (haute priorité)
        rfp_indicators = [
            'marché public', "appel d'offres", 'date limite de remise',
            'critères de sélection', 'budget annuel', 'lot n°', 'lot 1',
            'pénalités', 'clause', 'soumissionnaire', 'candidat',
            'procédure', 'règlement de consultation', 'cctp', 'dce',
            "acte d'engagement", 'dc1', 'dc2', 'noti', 'mapa'
        ]
        
        rfp_score = sum(1 for indicator in rfp_indicators if indicator in content_lower)
        
        if rfp_score >= 3:
            return {
                "input_type": input_type,
                "suggested_action": "summarize",
                "suggestion_reason": f"💡 Détecté: Appel d'offres ({rfp_score} indicateurs trouvés). Analyse RFP recommandée.",
                "confidence": min(0.95, 0.5 + (rfp_score * 0.1)),
                "alternative_actions": ["deck", "diagram"],
                "source_info": source_info
            }
        
        # Détection 2: Contenu technique / Architecture
        technical_indicators = [
            'architecture', 'infrastructure', 'diagramme', 'schéma',
            'serveur', 'réseau', 'cloud', 'aws', 'azure', 'gcp',
            'microservice', 'api', 'base de données', 'kubernetes',
            'docker', 'composant', 'module', 'flux de données'
        ]
        
        tech_score = sum(1 for indicator in technical_indicators if indicator in content_lower)
        
        if tech_score >= 3:
            return {
                "input_type": input_type,
                "suggested_action": "diagram",
                "suggestion_reason": f"💡 Détecté: Contenu technique ({tech_score} éléments). Diagramme d'architecture recommandé.",
                "confidence": min(0.85, 0.5 + (tech_score * 0.08)),
                "alternative_actions": ["deck", "summarize"],
                "source_info": source_info
            }
        
        # Détection 3: Demande de présentation explicite
        presentation_keywords = [
            'présentation', 'powerpoint', 'slides', 'deck', 'ppt',
            'créer une présentation', 'générer des slides', 'faire un deck'
        ]
        
        if any(keyword in content_lower for keyword in presentation_keywords):
            return {
                "input_type": input_type,
                "suggested_action": "deck",
                "suggestion_reason": "💡 Détecté: Demande de création de présentation PowerPoint.",
                "confidence": 0.9,
                "alternative_actions": ["diagram", "summarize"],
                "source_info": source_info
            }
        
        # Détection 4: Demande explicite d'analyse RFP
        rfp_request_keywords = [
            'analyser', 'résumer', 'rfp', "appel d'offres", 'ao',
            'analyse ce rfp', 'résume cet appel'
        ]
        
        if any(keyword in content_lower for keyword in rfp_request_keywords):
            return {
                "input_type": input_type,
                "suggested_action": "summarize",
                "suggestion_reason": "💡 Détecté: Demande d'analyse d'appel d'offres.",
                "confidence": 0.85,
                "alternative_actions": ["deck", "diagram"],
                "source_info": source_info
            }
        
        # Détection 5: Contenu long et structuré → Présentation
        if len(analysis_content) > 500:
            return {
                "input_type": input_type,
                "suggested_action": "deck",
                "suggestion_reason": "💡 Contenu détecté. Je peux créer une présentation PowerPoint professionnelle.",
                "confidence": 0.7,
                "alternative_actions": ["summarize", "diagram"],
                "source_info": source_info
            }
    
    # Détection par règles terminée
    rule_based_result = {
        "input_type": input_type,
        "suggested_action": None,
        "suggestion_reason": "Choisissez l'action qui convient le mieux à votre besoin.",
        "confidence": 0.0,
        "alternative_actions": ["summarize", "deck", "diagram", "harmonize"],
        "source_info": source_info
    }
    
    # Si use_ai=True ET qu'on a du contenu à analyser, utiliser l'IA
    if use_ai and analysis_content and len(analysis_content) > 50:
        print(f"🧠 Analyse IA activée pour améliorer la détection...")
        ai_result = await analyze_content_with_ai(
            content=analysis_content,
            filename=filename
        )
        
        if ai_result:
            # Fusionner les résultats IA + règles
            return merge_ai_and_rule_based_detection(ai_result, rule_based_result)
    
    # Pas d'IA ou contenu trop court - retourner détection par règles
    rule_based_result["detection_method"] = "rules"
    rule_based_result["ai_powered"] = False
    return rule_based_result

def _get_alternative_actions(suggested_action: Optional[str]) -> list:
    """Obtenir les actions alternatives basées sur la suggestion"""
    all_actions = ["summarize", "deck", "diagram", "harmonize"]
    
    if not suggested_action:
        return all_actions
    
    # Retourner toutes les actions sauf celle suggérée
    return [action for action in all_actions if action != suggested_action]

