"""
Agent Deck Generator
Génère des présentations PowerPoint complètes avec IA (niveau skywork.ai)

Deux approches disponibles:
1. JSON → PPTX (approche classique, rapide)
2. HTML/CSS → PPTX (approche skywork.ai, qualité supérieure avec validation loop)
"""
from .deck_generator import generate_deck_plan_with_ai
from .infotel_template_builder import create_powerpoint_from_template

# NOUVEAU: Approche HTML/CSS (skywork.ai level)
from .html_deck_generator import (
    generate_html_deck_with_ai,
    validate_html_deck,
    generate_and_validate_html_deck
)
from .html_to_pptx_converter import html_to_editable_pptx, parse_html_to_structure

# Backup builder (compatibilité)
from .pptx_deck_builder import create_powerpoint_deck

__all__ = [
    # Approche classique (JSON → PPTX)
    'generate_deck_plan_with_ai',
    'create_powerpoint_from_template',
    'create_powerpoint_deck',
    
    # Approche skywork.ai (HTML/CSS → PPTX avec validation)
    'generate_html_deck_with_ai',
    'validate_html_deck',
    'generate_and_validate_html_deck',
    'html_to_editable_pptx',
    'parse_html_to_structure'
]

