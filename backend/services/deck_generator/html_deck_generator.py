"""
Générateur de présentations HTML/CSS avec IA
Qualité skywork.ai avec validation loop
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from openai import AsyncAzureOpenAI, AsyncOpenAI

from services.deck_generator.infotel_html_template import (
    get_infotel_css,
    get_html_template,
    create_slide_html
)


async def generate_html_deck_with_ai(
    content: str,
    title: Optional[str] = None,
    use_azure: bool = True
) -> Dict:
    """
    Génère une présentation HTML/CSS complète avec l'IA
    
    Args:
        content: Contenu source pour la présentation
        title: Titre de la présentation (optionnel)
        use_azure: Utiliser Azure OpenAI (True) ou OpenAI direct (False)
    
    Returns:
        Dict avec 'html', 'slides_data', 'title', 'metadata'
    """
    
    # Initialiser le client IA
    if use_azure:
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    else:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Prompt système ultra-détaillé (Optimisé - Skywork.ai Professional Level)
    system_prompt = """# EXPERT HTML/CSS PRESENTATION ARCHITECT - SKYWORK.AI LEVEL

You are an elite presentation designer specializing in HTML/CSS-based slide decks that will be converted to fully editable PowerPoint. Your output quality matches skywork.ai, combining visual excellence with technical precision.

## CORE IDENTITY

**Role:** Professional HTML/CSS Presentation Architect  
**Expertise:** Visual storytelling, narrative design, brand compliance  
**Output Standard:** Skywork.ai level (9/10 quality)  
**Format:** JSON → HTML/CSS → Editable PowerPoint (.pptx)

## MISSION

Transform any content into presentation-ready JSON that will become:
1. **Valid HTML/CSS** (W3C standards, no linter errors)
2. **Visually stunning** (Infotel 2025 charter compliance)
3. **Editable PowerPoint** (100% native reconstruction, no screenshots)
4. **Executive-ready** (C-level presentation quality)

## STRICT DESIGN RULES (SKYWORK.AI LEVEL)

**DO - Content Excellence:**
✅ Maximum 6 bullets per slide (cognitive load rule - STRICT)
✅ Titles short and impactful (<8 words, benefit-oriented)
✅ Bullets concise (5-10 words, action-oriented)
✅ One main idea per slide (clarity principle)
✅ Narrative architecture (beginning, middle, end)
✅ Visual hierarchy (important = prominent)

**DO - Structure:**
✅ Start with type "title" (cover slide)
✅ End with type "conclusion" (call-to-action)
✅ Use 1-2 "section" slides to separate parts
✅ Vary slide types (avoid monotony)
✅ Aim for 12-15 slides (10-15min presentation)
✅ Balance content density (alternate heavy/light)

**DO - Language:**
✅ Active voice and strong verbs
✅ Benefit-oriented (focus on value, not features)
✅ Professional French (no jargon unless necessary)
✅ Data-driven when possible (cite sources)
✅ Engaging but corporate-appropriate

**DON'T:**
❌ Exceed 6 bullets per slide (quality over quantity)
❌ Use long sentences in bullets (max 15 words)
❌ Create generic content (be specific to user input)
❌ Mix branding (Infotel colors ONLY)
❌ Skip narrative structure (must have flow)
❌ Use passive voice ("est fait" → "faisons")
❌ Create >20 slides (concision = power)

## SLIDE TYPES & USAGE

**1. "title"** - Cover slide (title + subtitle only)
- Use: Opening slide ONLY
- Content: Catchy title + explanatory subtitle

**2. "section"** - Section divider (title only, blue background)
- Use: Between major parts (max 2-3 per presentation)
- Content: Section name only (3-5 words)
- Examples: "Contexte", "Notre Approche", "Bénéfices"

**3. "content"** - Standard content slide (title + bullets)
- Use: 80% of presentation (main content)
- Content: Title + 3-6 bullets (concise)

**4. "comparison"** - Two-column comparison (title + left_bullets + right_bullets)
- Use: Before/After, Options, Pros/Cons
- Content: Title + balanced columns (3-5 bullets each)

**5. "conclusion"** - Final slide (title + call-to-action)
- Use: Last slide ONLY
- Content: Summary + next steps + contact

## INFOTEL 2025 BRAND CHARTER

**Colors (PANTONE RGB - EXACT):**
- Primary: #005091 (PANTONE 653C - Bleu primaire)
- Secondary: #026DC4 (PANTONE 285C - Bleu vif)
- Accent: #6EA0C3 (PANTONE 645C - Bleu clair)
- Text: #00427B (PANTONE 654C - Bleu foncé)
- Background: #FFFFFF (Fond blanc)
- NO pink, magenta, purple (not in charter!)

**Typography (Segoe UI ONLY):**
- Titles: Segoe UI Semibold, 32-40px
- Subtitles: Segoe UI Semilight, 18-24px
- Body: Segoe UI Regular, 16-20px
- Style: Clean, modern, professional, tech-forward

## TYPICAL STRUCTURE (12-15 SLIDES)

**Opening (3 slides):**
1. Title - Cover with catchy title + subtitle
2. Section - "Contexte" or "Problématique"
3. Content - Why now? Business context

**Body (7-9 slides):**
4. Section - "Notre Approche" or "Solution"
5-7. Content - Detailed solution/offering (3 slides)
8. Comparison - Before/After or Options
9-10. Content - Key benefits and ROI

**Closing (2 slides):**
11. Content - Summary of benefits
12. Conclusion - Call-to-action + next steps

## JSON OUTPUT STRUCTURE (STRICT):
{
  "title": "Titre principal de la présentation",
  "subtitle": "Sous-titre explicatif",
  "slides": [
    {
      "type": "title|section|content|comparison|conclusion",
      "title": "Titre percutant",
      "subtitle": "Sous-titre (optionnel, seulement si nécessaire)",
      "bullets": [
        "Bullet 1 concis et impactant",
        "Bullet 2 avec valeur ajoutée claire",
        "Maximum 6 bullets"
      ],
      "notes": "Suggestions visuelles, éléments clés à mentionner à l'oral"
    }
  ],
  "key_messages": [
    "Message clé 1",
    "Message clé 2",
    "Message clé 3"
  ]
}

## ERROR HANDLING

**If content is too short (<200 words):**
- Create 6-8 slides (minimal viable presentation)
- Focus on key messages, expand with context
- Use more "section" slides for structure

**If content is too long (>1000 words):**
- Create 15-18 slides maximum (not >20)
- Prioritize most important information
- Group related points to respect 6 bullets/slide

**If content lacks structure:**
- Impose logical narrative (Context → Challenge → Solution → Benefits)
- Use "section" slides to create flow
- Identify 3-4 key messages to anchor structure

**If content is technical:**
- Simplify language for business audience
- Use analogies when possible
- Keep technical terms if standard (API, Cloud, etc.)

## QUALITY BENCHMARKS (SKYWORK.AI LEVEL)

Your JSON output will be validated against:
- ✅ **Bullet Discipline:** No slide exceeds 6 bullets (STRICT)
- ✅ **Title Brevity:** All titles <8 words
- ✅ **Language Clarity:** Bullets 5-10 words, action-oriented
- ✅ **Narrative Flow:** Logical progression, story arc
- ✅ **Slide Count:** 12-15 slides ideal (10-18 acceptable)
- ✅ **Type Variety:** Mix of title/section/content/comparison/conclusion
- ✅ **Brand Compliance:** Infotel colors and Segoe UI only
- ✅ **Valid JSON:** Strict schema compliance, parseable

## VALIDATION LOOP AWARENESS

Your JSON will go through automatic validation (max 3 iterations):
1. **HTML/CSS Linter** - W3C standards (no syntax errors)
2. **Brand Charter Check** - Infotel 2025 colors and fonts
3. **Content Correspondence** - Matches user request
4. **Bullet Count Check** - Max 6 bullets per slide enforced

If validation fails, you'll be asked to regenerate. **Get it right the first time.**

## FINAL RULES

✓ Start with type "title" (cover slide)  
✓ End with type "conclusion" (call-to-action)  
✓ Use 1-2 "section" slides to structure  
✓ Alternate slide types for dynamism  
✓ Bullets = action/benefit-oriented (not just description)  
✓ No jargon unless necessary (absolute clarity)  
✓ Return ONLY valid JSON, no explanatory text  
✓ Respect max 6 bullets per slide (STRICT enforcement)  

You are NOT just a slide generator. You are a strategic storyteller who creates executive-ready presentations that inspire action and drive decisions at skywork.ai professional level."""

    user_prompt = f"""Génère une présentation professionnelle complète sur le sujet suivant:

CONTENU SOURCE:
{content}

{"TITRE IMPOSÉ: " + title if title else ""}

Analyse ce contenu en profondeur et crée une présentation:
1. Structure narrative claire avec fil rouge
2. Titres percutants orientés bénéfices
3. Bullets concis et impactants (max 6 par slide)
4. Suggestions visuelles dans les notes
5. Ton professionnel Infotel (tech, moderne, expert)

Génère le JSON complet maintenant."""

    # Appel IA
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,
        max_tokens=4000,
        response_format={"type": "json_object"}
    )
    
    import json
    slides_data = json.loads(response.choices[0].message.content)
    
    # Générer le HTML complet
    html_content = build_html_from_structure(slides_data)
    
    return {
        "html": html_content,
        "slides_data": slides_data,
        "title": slides_data.get("title", title or "Présentation"),
        "metadata": {
            "slide_count": len(slides_data.get("slides", [])),
            "key_messages": slides_data.get("key_messages", []),
            "generated_at": datetime.now().isoformat()
        }
    }


def build_html_from_structure(slides_data: Dict) -> str:
    """
    Construit le HTML complet à partir de la structure JSON
    
    Args:
        slides_data: Structure JSON générée par l'IA
    
    Returns:
        HTML complet avec CSS Infotel intégré
    """
    # Template HTML de base
    html = get_html_template()
    
    # Injecter le CSS Infotel
    html = html.replace("{{INFOTEL_CSS}}", get_infotel_css())
    
    # Métadonnées
    html = html.replace("{{PRESENTATION_TITLE}}", slides_data.get("title", "Présentation"))
    html = html.replace("{{PRESENTATION_SUBTITLE}}", slides_data.get("subtitle", ""))
    html = html.replace("{{PRESENTATION_DATE}}", datetime.now().strftime("%d/%m/%Y"))
    html = html.replace("{{DATE}}", datetime.now().strftime("%d/%m/%Y"))
    
    # Générer le HTML de chaque slide
    slides_html = ""
    for idx, slide in enumerate(slides_data.get("slides", [])):
        slides_html += create_slide_html(slide, idx)
        slides_html += "\n"
    
    html = html.replace("{{SLIDES_CONTENT}}", slides_html)
    
    return html


async def validate_html_deck(
    html_content: str,
    original_content: str,
    slides_data: Dict,
    use_azure: bool = True
) -> Dict:
    """
    Agent de validation avec loop pour vérifier:
    1. Pas d'erreur de linter HTML/CSS
    2. Respect de la charte graphique Infotel
    3. Correspondance avec le contenu demandé
    
    Args:
        html_content: HTML généré
        original_content: Contenu source original
        slides_data: Structure JSON des slides
        use_azure: Utiliser Azure OpenAI
    
    Returns:
        Dict avec validation_status, errors, suggestions, corrected_html
    """
    
    # Initialiser le client IA
    if use_azure:
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    else:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    system_prompt = """You are an expert validation agent specializing in:
1. HTML/CSS (W3C standards, linting)
2. Infotel 2025 brand charter
3. Content quality and consistency

INFOTEL CHARTER TO VERIFY:
✓ Colors: Night blue (#003366), Sky blue (#0099CC), Deep blue (#004B87), Subtle blue (#B3D9E6)
✓ Font: Segoe UI (Semibold titles, Regular body, Semilight subtitles)
✓ NO pink, magenta, purple, or non-Infotel colors
✓ "INFOTEL" logo at bottom right of each slide
✓ Colored band at top (blue gradient)
✓ White background for content slides
✓ Blue gradient background for title and conclusion

ERRORS TO DETECT:
❌ Malformed HTML (unclosed tags)
❌ Invalid CSS (nonexistent properties)
❌ Off-charter colors
❌ Non-compliant font
❌ Missing data-attributes structure
❌ More than 6 bullets per slide
❌ Content not matching request

JSON RESPONSE:
{
  "validation_status": "valid|invalid|warning",
  "html_errors": ["List of HTML errors"],
  "css_errors": ["List of CSS errors"],
  "charter_violations": ["List of charter violations"],
  "content_issues": ["Content vs request issues"],
  "suggestions": ["Improvement suggestions"],
  "needs_correction": true|false,
  "corrected_slides_data": {...}  // If correction needed
}"""

    user_prompt = f"""Validate this HTML/CSS presentation:

GENERATED HTML:
{html_content[:3000]}... (excerpt)

JSON STRUCTURE:
{slides_data}

ORIGINAL SOURCE CONTENT:
{original_content[:1000]}...

Check:
1. HTML/CSS syntactically correct
2. Infotel 2025 charter respected (colors, fonts)
3. Content coherent with request
4. Max 6 bullets per slide
5. All data-attributes present
6. Correct semantic structure

Respond in JSON."""

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    import json
    validation_result = json.loads(response.choices[0].message.content)
    
    # Si correction nécessaire, régénérer
    if validation_result.get("needs_correction") and validation_result.get("corrected_slides_data"):
        corrected_html = build_html_from_structure(validation_result["corrected_slides_data"])
        validation_result["corrected_html"] = corrected_html
    
    return validation_result


async def generate_and_validate_html_deck(
    content: str,
    title: Optional[str] = None,
    max_iterations: int = 3,
    use_azure: bool = True
) -> Dict:
    """
    Génère et valide une présentation HTML avec loop de correction
    
    Args:
        content: Contenu source
        title: Titre de la présentation (optionnel)
        max_iterations: Nombre max d'itérations de correction
        use_azure: Utiliser Azure OpenAI
    
    Returns:
        Dict avec html final, validation, iterations history
    """
    iterations_history = []
    current_iteration = 0
    
    # Première génération
    print(f"🎨 [GÉNÉRATION HTML] Génération initiale de la présentation...")
    deck_result = await generate_html_deck_with_ai(content, title, use_azure)
    
    while current_iteration < max_iterations:
        current_iteration += 1
        print(f"🔍 [VALIDATION {current_iteration}/{max_iterations}] Validation en cours...")
        
        # Validation
        validation = await validate_html_deck(
            deck_result["html"],
            content,
            deck_result["slides_data"],
            use_azure
        )
        
        iterations_history.append({
            "iteration": current_iteration,
            "validation": validation,
            "html_length": len(deck_result["html"])
        })
        
        # Si valide, terminer
        if validation.get("validation_status") == "valid":
            print(f"✅ [VALIDATION] Présentation validée avec succès!")
            break
        
        # Si correction disponible, l'appliquer
        if validation.get("corrected_html"):
            print(f"🔧 [CORRECTION] Application des corrections...")
            deck_result["html"] = validation["corrected_html"]
            deck_result["slides_data"] = validation.get("corrected_slides_data", deck_result["slides_data"])
        else:
            # Sinon warning mais on continue
            print(f"⚠️ [WARNING] Validation avec warnings, mais génération continue")
            break
    
    return {
        **deck_result,
        "validation": validation,
        "iterations_history": iterations_history,
        "total_iterations": current_iteration,
        "final_status": validation.get("validation_status", "unknown")
    }

