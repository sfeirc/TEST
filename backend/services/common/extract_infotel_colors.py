"""
Configuration centrale des couleurs et styles du template PowerPoint Infotel
SOURCE UNIQUE DE VÉRITÉ pour la charte graphique Infotel

Ce fichier est la référence pour toutes les couleurs Infotel.
Tous les autres modules doivent importer depuis ici pour garantir la cohérence.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

# CHARTE GRAPHIQUE INFOTEL 2025 - Couleurs PANTONE officielles
# Format pour HTML/CSS et PowerPoint
INFOTEL_BRAND_COLORS = {
    'bleu_nuit': {     # PANTONE 653C
        'hex': '#003366',
        'rgb': (0, 51, 102)
    },
    'bleu_ciel': {     # PANTONE 285C
        'hex': '#0099CC',
        'rgb': (0, 153, 204)
    },
    'bleu_profond': {  # PANTONE 645C
        'hex': '#004B87',
        'rgb': (0, 75, 135)
    },
    'bleu_subtil': {   # PANTONE 654C
        'hex': '#B3D9E6',
        'rgb': (179, 217, 230)
    }
}

# Polices officielles Infotel
INFOTEL_FONTS = {
    'title': 'Segoe UI Semibold',
    'body': 'Segoe UI',
    'caption': 'Segoe UI Semilight'
}

def extract_colors_from_template(template_path: str):
    """
    Obtenir les couleurs officielles Infotel
    
    Args:
        template_path: Chemin vers le template PowerPoint Infotel (peut être vide)
    
    Returns:
        dict: Dictionnaire des couleurs RGBColor Infotel officielles
    
    Note:
        Cette fonction est la SOURCE UNIQUE DE VÉRITÉ pour les couleurs Infotel.
        Tous les builders et générateurs doivent utiliser ces couleurs.
    """
    
    # CHARTE GRAPHIQUE INFOTEL OFFICIELLE
    # Source: Charte graphique Infotel 2025 - Couleurs exactes avec PANTONE
    infotel_colors = {
        # Couleurs principales Infotel (ordre de priorité)
        "primary": RGBColor(0, 80, 145),      # Bleu Infotel #005091 - PANTONE 653C (C:100% M:60% J:0% N:20%)
        "blue_bright": RGBColor(2, 109, 196), # Bleu vif #026DC4 - PANTONE 285C (C:99% M:44% J:0% N:23%)
        "blue_light": RGBColor(110, 160, 195),# Bleu clair #6EA0C3 - PANTONE 645C (C:44% M:18% J:0% N:24%)
        "blue_dark": RGBColor(0, 66, 123),    # Bleu foncé #00427B - PANTONE 654C (C:100% M:46% J:0% N:52%)
        
        # Couleurs complémentaires
        "text": RGBColor(51, 51, 51),         # Gris foncé texte #333333
        "text_light": RGBColor(102, 102, 102),# Gris moyen #666666
        "background": RGBColor(255, 255, 255),# Blanc #FFFFFF
        "light_gray": RGBColor(242, 242, 242),# Gris très clair #F2F2F2
        
        # Aliases pour compatibilité
        "secondary": RGBColor(2, 109, 196),   # Alias de blue_bright
        "accent": RGBColor(110, 160, 195),    # Alias de blue_light (PAS DE ROSE!)
        "dark": RGBColor(0, 66, 123),         # Alias de blue_dark
    }
    
    return infotel_colors

def get_infotel_fonts():
    """
    Polices standards Infotel (charte graphique officielle 2025)
    
    Returns:
        dict: Polices Segoe UI avec leurs variantes exactes de la charte
    """
    return {
        # Polices officielles Infotel (Segoe UI uniquement)
        "regular": "Segoe UI",              # Segoe UI Regular - Texte standard
        "semilight": "Segoe UI Semilight",  # Segoe UI Semilight - Texte léger
        "semibold": "Segoe UI Semibold",    # Segoe UI Semibold - Titres et emphase
        
        # Aliases pour compatibilité avec le code existant
        "title": "Segoe UI Semibold",       # Titres principaux
        "heading": "Segoe UI Semibold",     # Sous-titres
        "body": "Segoe UI",                 # Corps de texte
        "caption": "Segoe UI Semilight"     # Légendes
    }

if __name__ == "__main__":
    colors = extract_colors_from_template("")
    print("🎨 Couleurs Infotel extraites:")
    for name, color in colors.items():
        print(f"  {name}: RGB({color.r}, {color.g}, {color.b})")

