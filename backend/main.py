from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import re
from dotenv import load_dotenv
import tempfile

# Import services par agent (structure organisée)
from services.rfp_summarizer import (
    extract_text_from_file,
    extract_text_from_sharepoint,
    summarize_rfp_with_ai,
    is_sharepoint_url
)

load_dotenv()

app = FastAPI(title="Infotel RFP Summarizer API")

# CORS middleware for Teams integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class SummarizeRfpRequest(BaseModel):
    rfpText: str

# Response model is now flexible to accommodate the detailed French structure
SummarizeRfpResponse = dict  # Returns the full JSON structure from AI

# Helper function to detect and strip slash commands
def detect_and_strip_command(text: str) -> tuple[str, str]:
    """
    Detect slash commands and strip them from text
    Returns: (command, cleaned_text)
    """
    if not text:
        return ("", "")
    
    # Check for slash commands or number commands at start of text
    command_patterns = {
        # Slash commands
        r'^/summarize\s*': 'summarize',
        r'^/rfp\s*': 'summarize',
        r'^/analyze\s*': 'summarize',
        r'^/diagram\s*': 'diagram',
        r'^/diagramme\s*': 'diagram',
        r'^/schema\s*': 'diagram',
        r'^/deck\s*': 'deck',
        r'^/presentation\s*': 'deck',
        r'^/slides\s*': 'deck',
        r'^/harmonize\s*': 'harmonize',
        r'^/standardize\s*': 'harmonize',
        # Number commands (1=summarize, 2=deck, 3=diagram, 4=harmonize)
        r'^1\s*': 'summarize',
        r'^2\s*': 'deck',
        r'^3\s*': 'diagram',
        r'^4\s*': 'harmonize',
    }
    
    detected_command = ""
    cleaned_text = text
    
    for pattern, command in command_patterns.items():
        if re.match(pattern, text, re.IGNORECASE):
            detected_command = command
            cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            break
    
    return (detected_command, cleaned_text)

@app.get("/")
async def root():
    return {
        "message": "API Infotel AI Agent",
        "version": "1.0.0",
        "endpoints": [
            "/summarizeRfp",
            "/generateDiagramFromText",
            "/generateDeckFromText",
            "/uniformizeProposal",
            "/download/{filename}"
        ],
        "status": {
            "summarizeRfp": "✅ Opérationnel",
            "generateDiagramFromText": "✅ Opérationnel",
            "generateDeckFromText": "✅ Opérationnel",
            "uniformizeProposal": "✅ Opérationnel"
        }
    }

@app.post("/summarizeRfp")
async def summarize_rfp(
    rfpText: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Résumer un appel d'offres à partir de:
    1. Texte direct (rfpText)
    2. Lien SharePoint (détecté dans rfpText)
    3. Upload de fichier (PDF, DOCX, TXT)
    """
    
    print("\n" + "="*60)
    print("🎯 ACTION APPELÉE: summarizeRfp")
    print("📝 Description: Analyser un appel d'offres")
    print("="*60 + "\n")
    
    extracted_text = ""
    command_used = ""
    
    try:
        # Detect and strip slash commands from rfpText if present
        if rfpText:
            command_used, rfpText = detect_and_strip_command(rfpText)
            if command_used:
                print(f"🎯 Command detected: /{command_used}")
        
        # Priorité 1: Vérifier si un fichier est uploadé
        if file:
            print(f"📄 Traitement du fichier uploadé: {file.filename}")
            
            # Sauvegarder le fichier temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                extracted_text = extract_text_from_file(tmp_path, file.filename)
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        # Priorité 2: Vérifier si rfpText contient un lien SharePoint
        elif rfpText and is_sharepoint_url(rfpText):
            print(f"🔗 URL SharePoint détectée: {rfpText}")
            extracted_text = extract_text_from_sharepoint(rfpText.strip())
        
        # Priorité 3: Utiliser rfpText directement
        elif rfpText:
            print("📝 Traitement de l'entrée texte directe")
            extracted_text = rfpText
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Aucune entrée fournie. Veuillez fournir du texte, un lien SharePoint, ou uploader un fichier."
            )
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Le texte extrait est trop court ou vide. Veuillez fournir un document RFP valide."
            )
        
        # Résumer avec l'IA
        print(f"📊 Résumé de l'AO ({len(extracted_text)} caractères)...")
        if command_used:
            print(f"📋 Traitement avec la commande /{command_used}")
        summary = await summarize_rfp_with_ai(extracted_text)
        
        print("✅ ACTION TERMINÉE: summarizeRfp")
        print("="*60 + "\n")
        
        return summary
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors du traitement de l'AO: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement de l'AO: {str(e)}"
        )

@app.post("/generateDiagramFromText")
async def generate_diagram(
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Générer un diagramme PowerPoint professionnel à partir de texte ou fichier
    
    Entrée:
    - description: Description textuelle de ce qu'il faut schématiser
    - file: Fichier optionnel dont extraire le contenu
    
    Sortie:
    - Spécification du diagramme + URL de téléchargement du fichier PowerPoint
    """
    
    print("\n" + "="*60)
    print("🎯 ACTION APPELÉE: generateDiagramFromText")
    print("🎨 Description: Créer un diagramme d'architecture")
    print("="*60 + "\n")
    
    from services.diagram_generator import generate_diagram_spec_with_ai, create_powerpoint_diagram
    
    extracted_text = ""
    command_used = ""
    
    try:
        # Détecter et retirer les commandes
        if description:
            command_used, description = detect_and_strip_command(description)
            if command_used:
                print(f"🎯 Commande détectée: /{command_used}")
        
        # Priorité 1: Upload de fichier
        if file:
            print(f"📄 Traitement du fichier pour diagramme: {file.filename}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                # extract_text_from_file déjà importé en haut
                extracted_text = extract_text_from_file(tmp_path, file.filename)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        # Priorité 2: Lien SharePoint
        elif description and is_sharepoint_url(description):
            print(f"🔗 URL SharePoint détectée pour diagramme")
            # extract_text_from_sharepoint déjà importé en haut
            extracted_text = extract_text_from_sharepoint(description.strip())
        
        # Priorité 3: Texte direct
        elif description:
            extracted_text = description
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Veuillez fournir une description ou uploader un fichier"
            )
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Le contenu est trop court pour générer un diagramme"
            )
        
        # Générer la spécification du diagramme avec l'IA
        print(f"🎨 Génération du diagramme à partir de {len(extracted_text)} caractères...")
        diagram_spec = await generate_diagram_spec_with_ai(extracted_text)
        
        # Créer le fichier PowerPoint
        os.makedirs("generated_files", exist_ok=True)
        import uuid
        file_id = str(uuid.uuid4())[:8]
        filename = f"diagram_{file_id}.pptx"
        output_path = os.path.join("generated_files", filename)
        
        create_powerpoint_diagram(diagram_spec, output_path)
        
        print("✅ ACTION TERMINÉE: generateDiagramFromText")
        print(f"📦 Fichier PowerPoint créé: {filename}")
        print("="*60 + "\n")
        
        # Retourner la spécification + URL de téléchargement
        result = {
            **diagram_spec,
            "powerpoint_file": filename,
            "download_url": f"/download/{filename}"
        }
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la génération du diagramme: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Échec de la génération du diagramme: {str(e)}"
        )

@app.post("/generateDeckFromText")
async def generate_deck(
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    confirm_plan: Optional[str] = Form("false"),  # "true" ou "false" en string
    html_id: Optional[str] = Form(None)  # ID du HTML temporaire pour conversion
):
    """
    Générer une présentation PowerPoint à partir de texte ou fichier
    
    NOUVELLE APPROCHE HTML/CSS (niveau skywork.ai):
    1. Génère HTML/CSS avec IA
    2. Valide avec agent loop (linter + charte + contenu)
    3. Prévisualisation dans Teams
    4. Conversion HTML → PowerPoint ÉDITABLE
    
    Workflow en 2 étapes:
    1. Si confirm_plan=false (défaut): Génère HTML et demande confirmation
    2. Si confirm_plan=true: Convertit HTML en fichier PowerPoint ÉDITABLE
    
    Entrée:
    - description: Description textuelle ou contenu
    - file: Fichier optionnel dont extraire le contenu
    - confirm_plan: "true" pour générer le fichier, "false" pour juste le HTML
    - html_id: ID du HTML temporaire (pour conversion en étape 2)
    
    Sortie:
    - Si confirm_plan=false: HTML validé + plan pour prévisualisation
    - Si confirm_plan=true: URL de téléchargement du fichier PowerPoint ÉDITABLE
    """
    
    print("\n" + "="*60)
    print("🎯 ACTION APPELÉE: generateDeckFromText (HTML/CSS)")
    print(f"📊 Mode: {'Conversion HTML→PPTX' if confirm_plan == 'true' else 'Génération HTML+Validation'}")
    print("="*60 + "\n")
    
    extracted_text = ""
    command_used = ""
    confirm_generation = (confirm_plan == "true")
    
    try:
        # Détecter et retirer les commandes
        if description:
            command_used, description = detect_and_strip_command(description)
            if command_used:
                print(f"🎯 Commande détectée: /{command_used}")
        
        # Priorité 1: Upload de fichier
        if file:
            print(f"📄 Traitement du fichier pour présentation: {file.filename}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                extracted_text = extract_text_from_file(tmp_path, file.filename)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        # Priorité 2: Lien SharePoint
        elif description and is_sharepoint_url(description):
            print(f"🔗 URL SharePoint détectée pour présentation")
            extracted_text = extract_text_from_sharepoint(description.strip())
        
        # Priorité 3: Texte direct
        elif description:
            extracted_text = description
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Veuillez fournir une description ou uploader un fichier"
            )
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Le contenu est trop court pour générer une présentation"
            )
        
        from services.deck_generator import (
            generate_and_validate_html_deck,
            html_to_editable_pptx,
            parse_html_to_structure
        )
        import json
        import uuid
        
        # ÉTAPE 1: Génération HTML + Validation avec loop
        if not confirm_generation:
            # Mode: Générer HTML/CSS avec validation loop
            print(f"🎨 Génération HTML/CSS à partir de {len(extracted_text)} caractères...")
            print(f"🔍 Validation automatique avec loop (max 3 itérations)...")
            
            html_result = await generate_and_validate_html_deck(
                content=extracted_text,
                title=None,  # L'IA va le générer
                max_iterations=3,
                use_azure=True
            )
            
            # Sauvegarder le HTML temporairement pour conversion ultérieure
            html_id = str(uuid.uuid4())[:8]
            os.makedirs("generated_files", exist_ok=True)
            html_path = os.path.join("generated_files", f"presentation_{html_id}.html")
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_result['html'])
            
            print(f"✅ HTML généré et validé!")
            print(f"📊 Slides: {html_result['metadata']['slide_count']}")
            print(f"🔄 Itérations de validation: {html_result['total_iterations']}")
            print(f"✅ Status final: {html_result['final_status']}")
            
            validation = html_result.get('validation', {})
            if validation.get('html_errors'):
                print(f"⚠️ Erreurs HTML: {validation['html_errors']}")
            if validation.get('css_errors'):
                print(f"⚠️ Erreurs CSS: {validation['css_errors']}")
            if validation.get('charter_violations'):
                print(f"⚠️ Violations charte: {validation['charter_violations']}")
            
            print("="*60 + "\n")
            
            # Extraire la structure pour l'Adaptive Card
            structure = parse_html_to_structure(html_result['html'])
            
            # Retourner le plan + HTML ID pour conversion
            result = {
                "title": html_result['title'],
                "slides": structure['slides'],
                "key_messages": html_result['metadata'].get('key_messages', []),
                "html_id": html_id,
                "html_preview_url": f"/preview-html/{html_id}",
                "validation_status": html_result['final_status'],
                "validation_iterations": html_result['total_iterations'],
                "status": "html_ready",
                "message": "🎨 HTML généré et validé. Confirmez pour créer le PowerPoint.",
                "requires_confirmation": True
            }
            
            return result
        
        else:
            # Mode: Convertir HTML → PowerPoint ÉDITABLE
            print(f"🔄 Conversion HTML → PowerPoint ÉDITABLE...")
            
            # Récupérer le HTML temporaire
            if not html_id:
                raise HTTPException(
                    status_code=400,
                    detail="html_id manquant pour la conversion. Veuillez régénérer le plan."
                )
            
            html_path = os.path.join("generated_files", f"presentation_{html_id}.html")
            
            if not os.path.exists(html_path):
                raise HTTPException(
                    status_code=404,
                    detail="HTML temporaire introuvable. Veuillez régénérer le plan."
                )
            
            # Lire le HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Créer le fichier PowerPoint ÉDITABLE à partir du HTML
            file_id = str(uuid.uuid4())[:8]
            filename = f"presentation_{file_id}.pptx"
            output_path = os.path.join("generated_files", filename)
            
            print(f"🎨 Parsing HTML et reconstruction PowerPoint natif...")
            html_to_editable_pptx(html_content, output_path)
            
            # Nettoyer le HTML temporaire
            try:
                os.remove(html_path)
            except:
                pass
            
            print("✅ ACTION TERMINÉE: generateDeckFromText (HTML/CSS)")
            print(f"📦 PowerPoint ÉDITABLE créé: {filename}")
            print("="*60 + "\n")
            
            # Extraire la structure pour l'Adaptive Card
            structure = parse_html_to_structure(html_content)
            
            # Retourner le résultat avec URL de téléchargement
            result = {
                "title": structure['title'],
                "slides": structure['slides'],
                "powerpoint_file": filename,
                "download_url": f"/download/{filename}",
                "status": "completed",
                "message": "✅ PowerPoint ÉDITABLE généré avec succès (approche skywork.ai)!",
                "approach": "html_css_to_pptx",
                "editable": True
            }
            
            return result
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la génération de la présentation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Échec de la génération de la présentation: {str(e)}"
        )

@app.post("/uniformizeProposal")
async def uniformize_proposal(
    file: Optional[UploadFile] = File(None),
    template: Optional[str] = Form(None)
):
    """
    Harmoniser et standardiser une proposition PowerPoint selon la charte Infotel
    
    Entrée:
    - file: Fichier PowerPoint à harmoniser
    - template: Nom de template optionnel ou guide de style
    
    Sortie:
    - Spécification des slides harmonisées + URL de téléchargement du fichier PowerPoint
    """
    
    print("\n" + "="*60)
    print("🎯 ACTION APPELÉE: uniformizeProposal")
    print("🎨 Description: Harmoniser une proposition commerciale")
    print("="*60 + "\n")
    
    command_used = ""
    
    try:
        # Détecter les commandes dans le champ template
        if template:
            command_used, template = detect_and_strip_command(template)
            if command_used:
                print(f"🎯 Commande détectée: /{command_used}")
        
        if not file:
            raise HTTPException(
                status_code=400,
                detail="Veuillez uploader un fichier PowerPoint à harmoniser"
            )
        
        print(f"📄 Traitement du fichier PowerPoint: {file.filename}")
        
        # Sauvegarder le fichier temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Étape 1: Extraire le contenu du PowerPoint existant
            from services.proposal_harmonizer import extract_content_from_pptx, harmonize_presentation_with_ai
            
            print(f"📖 Extraction du contenu de {file.filename}...")
            extracted_content = extract_content_from_pptx(tmp_path)
            print(f"✅ {extracted_content['total_slides']} slides extraites")
            
            # Étape 2: Harmoniser avec l'IA
            print(f"🤖 Harmonisation intelligente avec IA...")
            harmonized_plan = await harmonize_presentation_with_ai(extracted_content)
            print(f"✅ Plan harmonisé: {harmonized_plan['harmonized_slides']} slides")
            
            # Étape 3: Recréer le PowerPoint avec le template Infotel
            from services.deck_generator import create_powerpoint_from_template
            
            os.makedirs("generated_files", exist_ok=True)
            import uuid
            file_id = str(uuid.uuid4())[:8]
            filename = f"harmonized_{file_id}.pptx"
            output_path = os.path.join("generated_files", filename)
            
            print(f"🎨 Création du PowerPoint harmonisé selon charte Infotel 2025...")
            create_powerpoint_from_template(harmonized_plan, output_path)
            
            print("✅ ACTION TERMINÉE: uniformizeProposal")
            print(f"📦 Fichier harmonisé créé: {filename}")
            print("="*60 + "\n")
            
            # Retourner le plan + URL de téléchargement
            result = {
                **harmonized_plan,
                "original_file": file.filename,
                "original_slides": extracted_content['total_slides'],
                "harmonized_file": filename,
                "download_url": f"/download/{filename}",
                "status": "success"
            }
            
            return result
        
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de l'harmonisation de la proposition: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Échec de l'harmonisation de la proposition: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Télécharger un fichier PowerPoint généré"""
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("generated_files", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=filename
    )

@app.get("/preview-html/{html_id}")
async def preview_html(html_id: str):
    """
    Prévisualiser le HTML généré avant conversion en PowerPoint
    
    Args:
        html_id: ID du fichier HTML temporaire
    
    Returns:
        HTML pour affichage dans le navigateur ou Teams
    """
    from fastapi.responses import HTMLResponse
    
    html_path = os.path.join("generated_files", f"presentation_{html_id}.html")
    
    if not os.path.exists(html_path):
        raise HTTPException(
            status_code=404,
            detail="HTML temporaire introuvable ou expiré"
        )
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

@app.get("/preview-standalone")
async def preview_standalone_page():
    """
    Page de prévisualisation standalone pour tester les templates HTML
    """
    from fastapi.responses import HTMLResponse
    
    html_path = "preview_standalone.html"
    
    if not os.path.exists(html_path):
        raise HTTPException(
            status_code=404,
            detail="Page de prévisualisation non trouvée"
        )
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

@app.post("/cleanup")
async def cleanup_temp_files_endpoint(max_age_hours: int = 24, dry_run: bool = False):
    """
    Nettoyer les fichiers temporaires anciens
    
    Args:
        max_age_hours: Âge maximum des fichiers en heures
        dry_run: Mode simulation
    
    Returns:
        Statistiques de nettoyage
    """
    from cleanup_temp_files import cleanup_old_files
    
    result = cleanup_old_files(
        directory="generated_files",
        max_age_hours=max_age_hours,
        dry_run=dry_run
    )
    
    return result

@app.post("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    return {"status": "opérationnel"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3001))
    uvicorn.run(app, host="0.0.0.0", port=port)

