"""
Module commun partagé par tous les agents
Contient la configuration de la charte graphique Infotel
et les utilitaires de détection intelligente de contenu (avec IA)
"""
from .extract_infotel_colors import extract_colors_from_template, get_infotel_fonts
from .file_type_detector import detect_file_purpose, get_content_preview, detect_content_intent
from .ai_content_analyzer import analyze_content_with_ai

__all__ = [
    'extract_colors_from_template', 
    'get_infotel_fonts',
    'detect_file_purpose',
    'get_content_preview',
    'detect_content_intent',
    'analyze_content_with_ai'
]

