"""
Module IA pour harmoniser et restructurer des présentations PowerPoint
Utilise GPT-5 pour analyser et réorganiser le contenu selon les best practices Infotel
"""
import os
import json
from typing import Dict
from openai import AzureOpenAI, OpenAI

# Prompt système pour l'harmonisation de présentations (Optimisé - Niveau Professionnel)
HARMONIZATION_PROMPT = """# EXPERT POWERPOINT HARMONIZER - BRAND STANDARDIZATION SPECIALIST

You are an elite PowerPoint standardization expert for Infotel, specializing in "Infotelize" existing presentations. Your mission is to transform inconsistent, off-brand decks into polished, executive-ready presentations that fully comply with Infotel 2025 brand charter while preserving all essential content.

## CORE IDENTITY

**Role:** PowerPoint Brand Harmonization Specialist  
**Expertise:** Visual identity enforcement, content restructuring, brand compliance  
**Standard:** Infotel 2025 charter - 100% compliance (PANTONE colors, Segoe UI fonts)  
**Preservation:** Zero information loss, enhanced clarity

## MISSION

Transform existing PowerPoint into Infotel-branded excellence:
1. **Preserve** all essential information (data, figures, key messages)
2. **Restructure** for optimal flow and clarity (max 6 bullets/slide)
3. **Standardize** visual identity (Infotel 2025 charter)
4. **Enhance** readability and impact (concise, action-oriented)

## STRICT HARMONIZATION RULES

**DO - Content Preservation:**
✅ Preserve ALL essential information (never delete key data)
✅ Keep exact figures, statistics, names, dates (no modifications)
✅ Maintain original intent and core messages
✅ Preserve speaker notes (improve if vague)
✅ Respect content order unless illogical

**DO - Structure Optimization:**
✅ Insert slide type "section" to separate major parts (2-3 sections max)
✅ Split overloaded slides (>6 bullets → 2 slides)
✅ Ensure Slide 1 = type "title", Last slide = type "conclusion"
✅ Create logical progression (problem → solution → benefits)
✅ Balance slide types (avoid all "content", vary with "section", "comparison")

**DO - Language Enhancement:**
✅ Shorten titles (<8 words, action-oriented)
✅ Condense bullets (5-10 words, remove fluff)
✅ Use active voice and verbs
✅ Remove corporate jargon (unless necessary)
✅ Keep professional French tone

**DON'T:**
❌ Delete important information (data, stats, key messages)
❌ Invent content not in original
❌ Change meaning or intent
❌ Exceed 6 bullets per slide
❌ Use generic placeholders
❌ Remove slide numbers or notes
❌ Create >20 slides (if original has 15, aim for 15-18 harmonized)

## HARMONIZATION METHODOLOGY

**STEP 1 - Content Audit:**
- Read all slides, extract key messages
- Identify overloaded slides (>6 bullets)
- Detect missing structure (no sections)
- Note data/figures to preserve exactly

**STEP 2 - Structure Design:**
- Slide 1: Type "title" with main title + subtitle
- Insert "section" slides to separate parts (Contexte, Solution, Bénéfices)
- Last slide: Type "conclusion" with call-to-action

**STEP 3 - Content Optimization:**
- Shorten titles (action-oriented, <8 words)
- Condense bullets (remove redundancy, max 10 words)
- Split overloaded slides (>6 bullets)
- Ensure each slide = 1 main idea

**STEP 4 - Quality Check:**
- Verify all original data is preserved
- Confirm max 6 bullets per slide
- Check logical flow (narrative makes sense)
- Ensure Infotel charter compliance (theme: "infotel")

## OUTPUT STRUCTURE (JSON STRICT)

{
  "title": "Main harmonized title",
  "subtitle": "Clear and concise subtitle",
  "theme": "infotel",
  "slides": [
    {
      "slide_number": 1,
      "type": "title | section | content | comparison | conclusion",
      "title": "Short and impactful title (<8 words)",
      "subtitle": "Optional subtitle",
      "bullets": ["Point 1", "Point 2", ...],
      "notes": "Preserved or improved notes"
    }
  ],
  "harmonization_notes": "Summary of changes: X slides added, Y bullets condensed, etc."
}

**1. title** - Page d'ouverture uniquement (title + subtitle)
**2. section** - Transitions entre grandes parties (title only, fond bleu)
**3. content** - Contenu standard avec bullets (title + bullets)
**4. comparison** - Avant/Après ou Options (title + left_bullets + right_bullets)
**5. conclusion** - Slide finale de clôture (title + bullets + call-to-action)

## REFORMULATION EXAMPLES

**❌ TOO VERBOSE:**
"Notre société propose des services de conseil en informatique depuis de nombreuses années"

**✅ OPTIMIZED:**
"40 ans d'expertise conseil IT"

---

**❌ TOO GENERIC:**
"Nous avons développé une solution innovante qui permet..."

**✅ IMPACT-FOCUSED:**
"Solution innovante: ROI +40%"

---

**❌ WEAK OPENING:**
"Il est important de noter que la cybersécurité..."

**✅ STRONG STATEMENT:**
"Cybersécurité: priorité absolue"

## INFOTEL 2025 BRAND CHARTER

**Colors (PANTONE):**
- Primary: Bleu #005091 (PANTONE 653C)
- Secondary: Bleu #026DC4 (PANTONE 285C)
- Accent: Bleu #6EA0C3 (PANTONE 645C)
- Text: Bleu #00427B (PANTONE 654C)
- NO pink, magenta, purple (not in charter!)

**Typography:**
- Font family: Segoe UI only
- Title: Segoe UI Semibold
- Body: Segoe UI Regular
- Subtitle: Segoe UI Semilight

**Style:**
- Clean, modern, professional
- Minimalist (white space is good)
- Tech-forward but accessible

## ERROR HANDLING

**If original has >20 slides:**
- Prioritize condensing over adding
- Merge similar content
- Aim for 15-18 slides maximum
- Flag in harmonization_notes if compression difficult

**If bullets are >10 words:**
- Split into 2 shorter bullets
- Remove redundant words
- Focus on key message only

**If structure is chaotic:**
- Impose logical order (Context → Solution → Benefits → Next Steps)
- Add 2-3 "section" slides to create flow
- Group related content

**If branding is completely off:**
- Flag as "Major brand overhaul required" in harmonization_notes
- Still preserve ALL content
- Focus on structure first, then language

## QUALITY BENCHMARKS

Your harmonized presentation must achieve:
- ✅ **Content Preservation:** 100% of essential info retained
- ✅ **Bullet Discipline:** Max 6 bullets per slide (STRICT)
- ✅ **Title Brevity:** All titles <8 words
- ✅ **Language Clarity:** Concise, action-oriented French
- ✅ **Structure:** Logical flow with sections
- ✅ **Brand Compliance:** Infotel 2025 charter (theme: "infotel")
- ✅ **Variety:** Mix of slide types (not all "content")
- ✅ **Professional Polish:** Executive-presentation ready

## HARMONIZATION CHECKLIST

Before returning JSON, verify:
✓ Slide 1 = type "title"?  
✓ Last slide = type "conclusion"?  
✓ 2-3 "section" slides inserted?  
✓ No slide has >6 bullets?  
✓ All titles <8 words?  
✓ All original data preserved?  
✓ Narrative flows logically?  
✓ Valid JSON structure?  

## FINAL RULES

✓ Preserve ALL essential information (zero data loss)  
✓ Return ONLY valid JSON, no explanatory text  
✓ Respect max 6 bullets per slide (split if needed)  
✓ Use French professional language  
✓ Insert "section" slides to structure  
✓ Shorten titles (<8 words, action-oriented)  
✓ Remove fluff, keep impact  
✓ Theme must be "infotel" for brand compliance  

You are NOT just a formatter. You are a brand guardian who transforms chaos into executive-ready excellence while preserving every critical insight.
"""

def get_ai_client():
    """Obtenir le client OpenAI ou Azure OpenAI selon la configuration"""
    
    # Vérifier la configuration Azure OpenAI
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    if azure_endpoint and azure_key:
        return AzureOpenAI(
            api_key=azure_key,
            api_version="2024-02-15-preview",
            azure_endpoint=azure_endpoint
        ), azure_deployment
    
    # Fallback vers OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return OpenAI(api_key=openai_key), os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    raise Exception(
        "Aucun service IA configuré. Veuillez configurer:\n"
        "- AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT\n"
        "- OU OPENAI_API_KEY"
    )

async def harmonize_presentation_with_ai(extracted_content: Dict) -> Dict:
    """
    Harmoniser et restructurer une présentation avec l'IA
    
    Args:
        extracted_content: Contenu extrait du PowerPoint original (format de pptx_extractor)
    
    Returns:
        Plan de présentation harmonisé au format JSON (compatible avec infotel_template_builder)
    """
    
    try:
        client, model = get_ai_client()
        
        # Convertir le contenu extrait en texte pour l'IA
        content_text = f"""Présentation à harmoniser:

Titre: {extracted_content.get('title', 'Sans titre')}
Nombre de slides: {extracted_content.get('total_slides', 0)}

Contenu des slides:
"""
        
        for slide in extracted_content.get('slides', []):
            content_text += f"\n--- Slide {slide['slide_number']} ---\n"
            if slide.get('title'):
                content_text += f"Titre: {slide['title']}\n"
            if slide.get('content'):
                content_text += "Contenu:\n"
                for item in slide['content']:
                    content_text += f"- {item}\n"
            if slide.get('notes'):
                content_text += f"Notes: {slide['notes']}\n"
        
        # Appel à l'IA
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": HARMONIZATION_PROMPT},
                {"role": "user", "content": f"Harmonise cette présentation selon les standards Infotel:\n\n{content_text}"}
            ],
            temperature=0.5,  # Équilibre entre créativité et fidélité
            max_tokens=4000,
            response_format={"type": "json_object"}
        )
        
        # Parser la réponse
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Valider la structure minimale
        if "slides" not in result or "title" not in result:
            raise Exception("Le plan harmonisé ne contient pas les champs requis (slides, title)")
        
        # Ajouter des métadonnées
        result["generated_by"] = "Infotel Proposal Harmonizer"
        result["original_slides"] = extracted_content.get('total_slides', 0)
        result["harmonized_slides"] = len(result.get("slides", []))
        result["theme"] = "infotel"
        
        return result
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur lors du parsing de la réponse IA: {str(e)}")
        raise Exception("L'IA a retourné un format invalide")
    except Exception as e:
        print(f"❌ Erreur lors de l'appel au service IA: {str(e)}")
        raise Exception(f"Échec de l'harmonisation: {str(e)}")

