"""
Analyseur de contenu basé sur l'IA (GPT-5)
Détecte intelligemment l'action la plus appropriée pour un document
"""
import os
import json
from typing import Dict, Optional
from openai import AzureOpenAI, OpenAI

# Prompt système pour l'analyse de contenu (Optimisé - Decision Tree Professional)
CONTENT_ANALYSIS_PROMPT = """# EXPERT CONTENT ANALYZER - INTELLIGENT ACTION ROUTING

You are an elite document analyzer for an AI agent orchestration system. Your mission is to instantly determine the BEST action for any uploaded content with high confidence and accuracy.

## CORE IDENTITY

**Role:** Content Analysis & Action Routing Specialist  
**Expertise:** Document classification, intent detection, pattern recognition  
**Output:** Confident action suggestion + reasoning  
**Standard:** 90%+ accuracy on action routing

## YOUR MISSION

Analyze uploaded content (file, link, or text) and route to 1 of 4 specialized agents:
1. **RFP Summarizer** - For tender documents requiring exhaustive analysis
2. **Deck Generator** - For content that should become presentations
3. **Diagram Generator** - For technical architectures needing visualization
4. **Proposal Harmonizer** - For existing PowerPoints needing standardization

## DECISION TREE (STRICT PRIORITY ORDER)

### STEP 1 - File Type Detection (HIGHEST PRIORITY)

**IF file extension = .pptx:**
→ **Action: "harmonize"**  
→ **Confidence: 0.95**  
→ **Reason: "Fichier PowerPoint détecté - harmonisation automatique selon charte Infotel"**  
→ STOP (don't analyze content)

### STEP 2 - RFP Indicators (SECOND PRIORITY)

**IF content contains ≥3 of these indicators:**
- "appel d'offres" or "marché public"
- "consultation" + "lot" + "budget"
- "critères de sélection" or "grille d'évaluation"
- "date limite de remise" or "calendrier soumission"
- "cahier des charges" or "dossier de consultation"
- "pénalités" + "reconduction" + "résiliation"
- "mémoire technique" + "offre financière"

→ **Action: "summarize"**  
→ **Confidence: 0.85-0.95** (based on indicator count)  
→ **Reason: "Document d'appel d'offres détecté - analyse RFP complète requise"**  
→ STOP (high confidence, no need to continue)

### STEP 3 - Technical Architecture (THIRD PRIORITY)

**IF content contains ≥4 of these indicators:**
- Technical terms: "architecture", "infrastructure", "serveur"
- Cloud: "AWS", "Azure", "GCP", "Kubernetes", "Docker"
- Components: "API", "microservices", "base de données"
- Network: "réseau", "load balancer", "firewall"
- Stack: "frontend", "backend", "middleware", "cache"

→ **Action: "diagram"**  
→ **Confidence: 0.75-0.90** (based on technical density)  
→ **Reason: "Architecture technique détectée - diagramme professionnel recommandé"**

### STEP 4 - Presentation Content (DEFAULT)

**IF content is:**
- Long-form text (>500 words)
- Structured with sections/headings
- Business/corporate topic
- Narrative or explanatory
- No strong RFP or technical indicators

→ **Action: "deck"**  
→ **Confidence: 0.60-0.80** (varies with structure quality)  
→ **Reason: "Contenu adapté pour présentation - transformation en slides recommandée"**

### STEP 5 - Ambiguous/Too Short (FALLBACK)

**IF content is:**
- <100 words AND no clear indicators
- Random text with no structure
- Unclear intent

→ **Action: null**  
→ **Confidence: <0.50**  
→ **Reason: "Contenu insuffisant ou ambigu - précisez votre besoin svp"**

## OUTPUT FORMAT (JSON STRICT)

```json
{
  "suggested_action": "summarize" | "deck" | "diagram" | "harmonize" | null,
  "confidence": 0.0-1.0,
  "reason": "Explication en français (1-2 phrases, claire et actionnable)",
  "key_indicators": ["indicateur1", "indicateur2", "indicateur3"],
  "alternative_action": "action2" (ONLY if confidence <0.75 and viable alternative exists)
}
```

## CONFIDENCE THRESHOLDS

- **0.90-1.00:** Extremely confident (RFP keywords, .pptx extension, strong technical indicators)
- **0.75-0.89:** High confidence (multiple clear indicators)
- **0.60-0.74:** Moderate confidence (some indicators, but not overwhelming)
- **0.50-0.59:** Low confidence (few indicators, ambiguous)
- **<0.50:** No confidence (return null, ask user to clarify)

## STRICT RULES

**DO:**
✅ Follow decision tree in exact order (file type → RFP → technical → presentation)
✅ Count actual indicators (be factual, not interpretative)
✅ Return high confidence (>0.85) only with clear evidence
✅ Provide actionable reason in French
✅ List 3-5 key indicators found
✅ Return valid JSON only

**DON'T:**
❌ Guess or assume (base on actual content)
❌ Return multiple suggested_action (pick THE best one)
❌ Give high confidence without strong indicators
❌ Use English in "reason" field (French only)
❌ Analyze content if file is .pptx (auto-harmonize)
❌ Suggest "alternative_action" unless confidence <0.75

## EXAMPLES

**Example 1 - RFP:**
Content: "Marché public de services informatiques. Lot 1: Support applicatif. Date limite: 15/12/2024. Critères: prix 40%, technique 60%..."
→ {"suggested_action": "summarize", "confidence": 0.92, "reason": "Appel d'offres public avec lots et critères - analyse RFP complète", "key_indicators": ["marché public", "lot", "date limite", "critères"]}

**Example 2 - Architecture:**
Content: "Architecture microservices avec Kubernetes. Frontend React, backend Node.js, API REST, base PostgreSQL, cache Redis..."
→ {"suggested_action": "diagram", "confidence": 0.88, "reason": "Architecture technique avec composants multiples - diagramme d'architecture recommandé", "key_indicators": ["microservices", "Kubernetes", "API", "backend", "base de données"]}

**Example 3 - Presentation:**
Content: "Transformation digitale des entreprises. Contexte actuel, enjeux stratégiques, notre approche, bénéfices attendus, ROI..."
→ {"suggested_action": "deck", "confidence": 0.72, "reason": "Contenu corporate structuré - présentation PowerPoint recommandée", "key_indicators": ["structuré", "stratégique", "bénéfices", "approche"]}

**Example 4 - PowerPoint:**
Filename: "presentation_client.pptx"
→ {"suggested_action": "harmonize", "confidence": 0.95, "reason": "Fichier PowerPoint détecté - harmonisation selon charte Infotel", "key_indicators": [".pptx", "présentation existante"]}

**Example 5 - Ambiguous:**
Content: "Bonjour test"
→ {"suggested_action": null, "confidence": 0.20, "reason": "Contenu trop court pour déterminer l'action appropriée", "key_indicators": []}

## FINAL RULES

✓ Return ONLY valid JSON, no explanatory text  
✓ Reason in French (clear, actionable, 1-2 sentences)  
✓ Confidence matches evidence (don't overstate)  
✓ Key indicators = actual words/patterns found  
✓ Alternative action only if confidence <0.75  
✓ Be decisive (don't hedge with "maybe" or "possibly")  

You are NOT just a classifier. You are an intelligent routing engine that ensures each document reaches the RIGHT specialized agent for optimal processing.
"""

def get_ai_client():
    """Obtenir le client OpenAI ou Azure OpenAI"""
    # Vérifier Azure OpenAI
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    if azure_endpoint and azure_key:
        return AzureOpenAI(
            api_key=azure_key,
            api_version="2024-02-15-preview",
            azure_endpoint=azure_endpoint
        ), azure_deployment
    
    # Repli sur OpenAI Direct
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return OpenAI(api_key=openai_key), os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    return None, None

async def analyze_content_with_ai(
    content: str,
    filename: Optional[str] = None,
    max_content_length: int = 3000
) -> Dict:
    """
    Analyser le contenu avec l'IA pour suggérer l'action appropriée
    
    Args:
        content: Contenu à analyser (texte extrait du fichier)
        filename: Nom du fichier (optionnel, aide à la détection)
        max_content_length: Longueur max du contenu à envoyer à l'IA
    
    Returns:
        {
            "suggested_action": "summarize" | "deck" | "diagram" | "harmonize" | None,
            "confidence": 0.0-1.0,
            "reason": "Raison de la suggestion",
            "key_indicators": ["indicateur1", "indicateur2"],
            "alternative_action": "action2" (optionnel),
            "ai_powered": True
        }
    """
    
    try:
        client, model = get_ai_client()
        
        if not client:
            print("⚠️ Pas de service IA configuré, utilisation de la détection par mots-clés")
            return None
        
        # Tronquer le contenu si trop long (garder début + fin)
        if len(content) > max_content_length:
            half = max_content_length // 2
            content_to_analyze = content[:half] + "\n\n[... contenu tronqué ...]\n\n" + content[-half:]
        else:
            content_to_analyze = content
        
        # Ajouter le nom du fichier au contexte si disponible
        context = f"**Nom du fichier:** {filename}\n\n**Contenu:**\n\n{content_to_analyze}" if filename else content_to_analyze
        
        print(f"🧠 Analyse IA du contenu ({len(content)} caractères)...")
        
        # Appeler GPT-5 pour analyser
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": CONTENT_ANALYSIS_PROMPT},
                {"role": "user", "content": context}
            ],
            temperature=0.1,  # Faible température pour plus de cohérence
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # Parser la réponse
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Ajouter le flag AI-powered
        result["ai_powered"] = True
        
        print(f"✅ IA suggère: {result.get('suggested_action')} (confiance: {result.get('confidence', 0):.0%})")
        print(f"   Raison: {result.get('reason', 'N/A')}")
        
        return result
    
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing réponse IA: {str(e)}")
        return None
    
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse IA: {str(e)}")
        return None

def merge_ai_and_rule_based_detection(
    ai_result: Optional[Dict],
    rule_result: Dict
) -> Dict:
    """
    Fusionner les résultats de l'IA et des règles
    L'IA a priorité si disponible et confiance >70%
    
    Args:
        ai_result: Résultat de l'analyse IA (ou None)
        rule_result: Résultat de la détection par règles
    
    Returns:
        Résultat fusionné avec la meilleure suggestion
    """
    
    # Si pas d'IA ou échec, utiliser les règles
    if not ai_result:
        rule_result["detection_method"] = "rules"
        return rule_result
    
    # Si IA avec haute confiance (>70%), utiliser l'IA
    ai_confidence = ai_result.get("confidence", 0.0)
    if ai_confidence >= 0.7:
        return {
            "input_type": rule_result.get("input_type"),
            "suggested_action": ai_result.get("suggested_action"),
            "suggestion_reason": f"💡 IA: {ai_result.get('reason', '')}",
            "confidence": ai_confidence,
            "alternative_actions": rule_result.get("alternative_actions", []),
            "source_info": rule_result.get("source_info"),
            "key_indicators": ai_result.get("key_indicators", []),
            "detection_method": "ai",
            "ai_powered": True
        }
    
    # Si IA avec confiance moyenne (50-70%), mentionner les deux
    elif ai_confidence >= 0.5:
        return {
            "input_type": rule_result.get("input_type"),
            "suggested_action": ai_result.get("suggested_action"),
            "suggestion_reason": f"💡 IA suggère: {ai_result.get('reason', '')} (Confiance: {ai_confidence:.0%})",
            "confidence": ai_confidence,
            "alternative_actions": rule_result.get("alternative_actions", []),
            "source_info": rule_result.get("source_info"),
            "detection_method": "ai_moderate",
            "ai_powered": True
        }
    
    # Si IA avec faible confiance (<50%), utiliser les règles
    else:
        rule_result["detection_method"] = "rules_fallback"
        rule_result["ai_low_confidence"] = ai_confidence
        return rule_result

