"""
Template HTML/CSS pour génération de présentations Infotel
Charte graphique 2025 complète intégrée
"""

from services.common.extract_infotel_colors import INFOTEL_BRAND_COLORS

def get_infotel_css() -> str:
    """
    Retourne le CSS complet avec la charte Infotel 2025
    """
    return f"""
/* ============================================
   INFOTEL PRESENTATION CSS - CHARTE 2025
   ============================================ */

:root {{
    /* Couleurs PANTONE officielles */
    --infotel-bleu-nuit: {INFOTEL_BRAND_COLORS['bleu_nuit']['hex']};
    --infotel-bleu-ciel: {INFOTEL_BRAND_COLORS['bleu_ciel']['hex']};
    --infotel-bleu-profond: {INFOTEL_BRAND_COLORS['bleu_profond']['hex']};
    --infotel-bleu-subtil: {INFOTEL_BRAND_COLORS['bleu_subtil']['hex']};
    --infotel-blanc: #FFFFFF;
    --infotel-gris-clair: #F5F5F5;
    --infotel-gris-texte: #333333;
    
    /* Fonts officielles */
    --font-title: 'Segoe UI Semibold', 'Segoe UI', Arial, sans-serif;
    --font-body: 'Segoe UI', Arial, sans-serif;
    --font-caption: 'Segoe UI Semilight', 'Segoe UI Light', Arial, sans-serif;
    
    /* Dimensions standard PowerPoint (16:9) */
    --slide-width: 960px;
    --slide-height: 540px;
    --slide-padding: 40px;
    --slide-padding-top: 50px;
    --slide-padding-bottom: 60px;
}}

/* ============================================
   RESET & BASE
   ============================================ */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-body);
    background-color: #1a1a1a;
    padding: 20px;
    line-height: 1.6;
}}

/* ============================================
   CONTAINER PRINCIPAL
   ============================================ */
.presentation-container {{
    max-width: 1200px;
    margin: 0 auto;
}}

.presentation-header {{
    background: var(--infotel-bleu-nuit);
    color: white;
    padding: 30px;
    border-radius: 8px 8px 0 0;
    text-align: center;
}}

.presentation-header h1 {{
    font-family: var(--font-title);
    font-size: 32px;
    margin-bottom: 10px;
}}

.presentation-header .meta {{
    font-family: var(--font-caption);
    font-size: 14px;
    opacity: 0.9;
}}

/* ============================================
   SLIDES
   ============================================ */
.slide {{
    width: var(--slide-width);
    height: var(--slide-height);
    background: white;
    margin: 20px auto;
    padding: var(--slide-padding);
    padding-top: var(--slide-padding-top);
    padding-bottom: var(--slide-padding-bottom);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    border-radius: 0 0 8px 8px;
    position: relative;
    overflow: hidden;
    page-break-after: always;
}}

/* Header Infotel sur chaque slide */
.slide::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: linear-gradient(
        90deg, 
        var(--infotel-bleu-nuit) 0%, 
        var(--infotel-bleu-ciel) 50%,
        var(--infotel-bleu-profond) 100%
    );
}}

/* Logo Infotel en bas à droite */
.slide::after {{
    content: 'INFOTEL';
    position: absolute;
    bottom: 15px;
    right: 25px;
    font-family: var(--font-title);
    font-size: 11px;
    color: var(--infotel-bleu-nuit);
    letter-spacing: 2px;
    opacity: 0.7;
}}

/* Numéro de slide */
.slide-number {{
    position: absolute;
    bottom: 15px;
    left: 25px;
    font-family: var(--font-caption);
    font-size: 11px;
    color: var(--infotel-gris-texte);
    opacity: 0.5;
}}

/* ============================================
   SLIDE TITLE (Page de garde)
   ============================================ */
.slide[data-slide-type="title"] {{
    background: linear-gradient(
        135deg, 
        var(--infotel-bleu-nuit) 0%, 
        var(--infotel-bleu-profond) 100%
    );
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.slide[data-slide-type="title"]::after {{
    color: rgba(255, 255, 255, 0.5);
}}

.slide[data-slide-type="title"] .slide-title {{
    font-family: var(--font-title);
    font-size: 54px;
    margin-bottom: 30px;
    line-height: 1.2;
    font-weight: 600;
}}

.slide[data-slide-type="title"] .slide-subtitle {{
    font-family: var(--font-caption);
    font-size: 24px;
    opacity: 0.9;
    margin-bottom: 60px;
}}

.slide[data-slide-type="title"] .slide-author {{
    font-family: var(--font-caption);
    font-size: 16px;
    opacity: 0.8;
    margin-top: 40px;
}}

.slide[data-slide-type="title"] .slide-date {{
    font-family: var(--font-caption);
    font-size: 14px;
    opacity: 0.7;
    margin-top: 10px;
}}

/* ============================================
   SLIDE SECTION (Séparateur)
   ============================================ */
.slide[data-slide-type="section"] {{
    background: var(--infotel-bleu-ciel);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.slide[data-slide-type="section"] .slide-title {{
    font-family: var(--font-title);
    font-size: 48px;
    text-align: center;
    font-weight: 600;
}}

/* ============================================
   SLIDE CONTENT (Contenu standard)
   ============================================ */
.slide[data-slide-type="content"] .slide-title {{
    font-family: var(--font-title);
    font-size: 36px;
    color: var(--infotel-bleu-nuit);
    margin-bottom: 30px;
    font-weight: 600;
    border-bottom: 3px solid var(--infotel-bleu-ciel);
    padding-bottom: 10px;
}}

.slide[data-slide-type="content"] .slide-subtitle {{
    font-family: var(--font-caption);
    font-size: 18px;
    color: var(--infotel-bleu-profond);
    margin-bottom: 20px;
    font-style: italic;
}}

/* Bullets */
.slide-content ul {{
    list-style: none;
    margin-left: 0;
    font-size: 20px;
    color: var(--infotel-gris-texte);
}}

.slide-content ul li {{
    position: relative;
    padding-left: 35px;
    margin-bottom: 18px;
    line-height: 1.5;
}}

/* Custom bullets avec couleur Infotel */
.slide-content ul li::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: var(--infotel-bleu-ciel);
    font-size: 24px;
    font-weight: bold;
}}

/* Sous-bullets */
.slide-content ul ul {{
    margin-top: 10px;
    margin-left: 20px;
}}

.slide-content ul ul li {{
    font-size: 18px;
    margin-bottom: 12px;
}}

.slide-content ul ul li::before {{
    content: '◦';
    font-size: 20px;
    color: var(--infotel-bleu-subtil);
}}

/* ============================================
   SLIDE COMPARISON (Comparaison 2 colonnes)
   ============================================ */
.slide[data-slide-type="comparison"] .slide-title {{
    font-family: var(--font-title);
    font-size: 32px;
    color: var(--infotel-bleu-nuit);
    margin-bottom: 25px;
    text-align: center;
    font-weight: 600;
}}

.comparison-container {{
    display: flex;
    gap: 30px;
    height: calc(100% - 120px);
}}

.comparison-column {{
    flex: 1;
    background: var(--infotel-gris-clair);
    padding: 25px;
    border-radius: 8px;
    border-top: 4px solid var(--infotel-bleu-ciel);
}}

.comparison-column h3 {{
    font-family: var(--font-title);
    font-size: 24px;
    color: var(--infotel-bleu-nuit);
    margin-bottom: 20px;
    font-weight: 600;
}}

.comparison-column ul {{
    list-style: none;
    font-size: 17px;
}}

.comparison-column ul li {{
    padding-left: 25px;
    margin-bottom: 12px;
    position: relative;
}}

.comparison-column ul li::before {{
    content: '✓';
    position: absolute;
    left: 0;
    color: var(--infotel-bleu-ciel);
    font-weight: bold;
}}

/* ============================================
   SLIDE CONCLUSION (Page de fin)
   ============================================ */
.slide[data-slide-type="conclusion"] {{
    background: linear-gradient(
        135deg, 
        var(--infotel-bleu-profond) 0%, 
        var(--infotel-bleu-nuit) 100%
    );
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.slide[data-slide-type="conclusion"] .slide-title {{
    font-family: var(--font-title);
    font-size: 48px;
    margin-bottom: 30px;
    font-weight: 600;
}}

.slide[data-slide-type="conclusion"] .slide-content {{
    font-family: var(--font-body);
    font-size: 22px;
    line-height: 1.6;
    max-width: 700px;
    margin-bottom: 40px;
}}

.slide[data-slide-type="conclusion"] .contact-info {{
    font-family: var(--font-caption);
    font-size: 16px;
    opacity: 0.9;
    margin-top: 30px;
}}

/* ============================================
   ÉLÉMENTS VISUELS
   ============================================ */

/* Encadré highlight */
.highlight-box {{
    background: var(--infotel-gris-clair);
    border-left: 4px solid var(--infotel-bleu-ciel);
    padding: 20px;
    margin: 20px 0;
    border-radius: 4px;
}}

.highlight-box strong {{
    color: var(--infotel-bleu-nuit);
}}

/* Texte important */
.important {{
    color: var(--infotel-bleu-nuit);
    font-weight: 600;
}}

/* Citation */
.quote {{
    font-family: var(--font-caption);
    font-size: 22px;
    font-style: italic;
    color: var(--infotel-bleu-profond);
    padding: 20px 40px;
    border-left: 4px solid var(--infotel-bleu-ciel);
    margin: 20px 0;
}}

/* Statistiques/chiffres clés */
.stat {{
    font-family: var(--font-title);
    font-size: 48px;
    color: var(--infotel-bleu-ciel);
    font-weight: 600;
    display: inline-block;
}}

/* ============================================
   RESPONSIVE & PRINT
   ============================================ */
@media print {{
    body {{
        background: white;
        padding: 0;
    }}
    
    .slide {{
        margin: 0;
        box-shadow: none;
        page-break-after: always;
    }}
    
    .presentation-header {{
        display: none;
    }}
}}

/* ============================================
   ANIMATIONS (pour prévisualisation web)
   ============================================ */
.slide {{
    animation: slideIn 0.3s ease-out;
}}

@keyframes slideIn {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* ============================================
   UTILITAIRES
   ============================================ */
.text-center {{
    text-align: center;
}}

.text-right {{
    text-align: right;
}}

.mb-small {{
    margin-bottom: 10px;
}}

.mb-medium {{
    margin-bottom: 20px;
}}

.mb-large {{
    margin-bottom: 40px;
}}

/* Conteneur pour colonnes */
.columns {{
    display: flex;
    gap: 30px;
}}

.column {{
    flex: 1;
}}
"""


def get_html_template() -> str:
    """
    Retourne le template HTML de base
    """
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="generator" content="Infotel AI Agents">
    <title data-editable="true">{{PRESENTATION_TITLE}}</title>
    <style>
        {{INFOTEL_CSS}}
    </style>
</head>
<body>
    <div class="presentation-container">
        <!-- En-tête de la présentation -->
        <div class="presentation-header">
            <h1 data-editable="true">{{PRESENTATION_TITLE}}</h1>
            <div class="meta">
                <span data-editable="true">{{PRESENTATION_SUBTITLE}}</span> • 
                <span data-editable="true">{{PRESENTATION_DATE}}</span>
            </div>
        </div>
        
        <!-- Slides générées par l'IA -->
        {{SLIDES_CONTENT}}
    </div>
    
    <script>
        // Script pour prévisualisation interactive (optionnel)
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Présentation Infotel chargée');
            
            // Ajouter numéros de slides
            const slides = document.querySelectorAll('.slide');
            slides.forEach((slide, index) => {
                if (!slide.querySelector('.slide-number')) {
                    const slideNumber = document.createElement('div');
                    slideNumber.className = 'slide-number';
                    slideNumber.textContent = `${index + 1} / ${slides.length}`;
                    slideNumber.setAttribute('data-editable', 'false');
                    slide.appendChild(slideNumber);
                }
            });
        });
    </script>
</body>
</html>
"""


def create_slide_html(slide_data: dict, slide_index: int) -> str:
    """
    Génère le HTML pour une slide individuelle
    
    Args:
        slide_data: Données de la slide (title, bullets, type, etc.)
        slide_index: Index de la slide (commence à 0)
    
    Returns:
        HTML de la slide
    """
    slide_type = slide_data.get('type', 'content')
    title = slide_data.get('title', '')
    subtitle = slide_data.get('subtitle', '')
    bullets = slide_data.get('bullets', [])
    notes = slide_data.get('notes', '')
    
    html = f'<div class="slide" data-slide-type="{slide_type}" data-slide-index="{slide_index}" data-notes="{notes}">\n'
    
    if slide_type == 'title':
        html += f'  <h1 class="slide-title" data-editable="true">{title}</h1>\n'
        if subtitle:
            html += f'  <p class="slide-subtitle" data-editable="true">{subtitle}</p>\n'
        html += f'  <p class="slide-author" data-editable="true">Infotel</p>\n'
        html += f'  <p class="slide-date" data-editable="true">{{DATE}}</p>\n'
    
    elif slide_type == 'section':
        html += f'  <h2 class="slide-title" data-editable="true">{title}</h2>\n'
    
    elif slide_type == 'conclusion':
        html += f'  <h2 class="slide-title" data-editable="true">{title}</h2>\n'
        if bullets:
            html += '  <div class="slide-content" data-editable="true">\n'
            html += f'    <p>{" ".join(bullets)}</p>\n'
            html += '  </div>\n'
        html += '  <div class="contact-info" data-editable="true">\n'
        html += '    <p>contact@infotel.com • www.infotel.com</p>\n'
        html += '  </div>\n'
    
    elif slide_type == 'comparison':
        html += f'  <h2 class="slide-title" data-editable="true">{title}</h2>\n'
        html += '  <div class="comparison-container">\n'
        # Split bullets en 2 colonnes
        mid = len(bullets) // 2
        col1 = bullets[:mid]
        col2 = bullets[mid:]
        
        html += '    <div class="comparison-column">\n'
        html += '      <h3 data-editable="true">Option A</h3>\n'
        html += '      <ul data-editable="true">\n'
        for bullet in col1:
            html += f'        <li>{bullet}</li>\n'
        html += '      </ul>\n'
        html += '    </div>\n'
        
        html += '    <div class="comparison-column">\n'
        html += '      <h3 data-editable="true">Option B</h3>\n'
        html += '      <ul data-editable="true">\n'
        for bullet in col2:
            html += f'        <li>{bullet}</li>\n'
        html += '      </ul>\n'
        html += '    </div>\n'
        html += '  </div>\n'
    
    else:  # 'content' (par défaut)
        html += f'  <h2 class="slide-title" data-editable="true">{title}</h2>\n'
        if subtitle:
            html += f'  <p class="slide-subtitle" data-editable="true">{subtitle}</p>\n'
        
        if bullets:
            html += '  <div class="slide-content">\n'
            html += '    <ul data-editable="true">\n'
            for bullet in bullets:
                html += f'      <li>{bullet}</li>\n'
            html += '    </ul>\n'
            html += '  </div>\n'
    
    html += '</div>\n'
    return html

