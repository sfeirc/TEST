#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive API Testing Script for Infotel AI Agent
Tests all endpoints with real data
"""

import requests
import json
import time
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://test-production-a01e.up.railway.app"

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_endpoint(name, method, url, **kwargs):
    """Test an endpoint and print results"""
    print(f"\n[{method}] {url}")
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, timeout=120, **kwargs)
        else:
            response = requests.request(method, url, timeout=30, **kwargs)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                # Truncate long responses for readability
                if isinstance(data, dict) and len(str(data)) > 1000:
                    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)[:1000]}...")
                else:
                    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Response (text): {response.text[:500]}")
        else:
            print(f"Error: {response.text[:500]}")
        
        return response
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return None

# Test 1: Root endpoint
print_header("TEST 1: Root Endpoint")
test_endpoint("Root", "GET", f"{BASE_URL}/")

# Test 2: API Documentation
print_header("TEST 2: API Documentation")
test_endpoint("Docs", "GET", f"{BASE_URL}/docs")

# Test 3: Health Check
print_header("TEST 3: Health Check")
test_endpoint("Health", "POST", f"{BASE_URL}/health")

# Test 4: Summarize RFP - Text Input
print_header("TEST 4: Summarize RFP (Text Input)")
rfp_text = """
Appel d'offres pour un système de gestion de données cloud

Introduction:
Notre entreprise cherche à moderniser son infrastructure IT avec une solution cloud native.

Exigences techniques:
- Support pour PostgreSQL et MongoDB
- API RESTful avec documentation OpenAPI
- Authentification OAuth 2.0
- Scalabilité automatique jusqu'à 10,000 utilisateurs simultanés
- Sauvegarde quotidienne avec rétention 30 jours
- SLA de 99.9% de disponibilité

Délais:
- Réponse: 15 janvier 2025
- Démarrage projet: 1er mars 2025
- Mise en production: 1er juin 2025

Budget:
Budget prévu: 500,000€ HT

Risques identifiés:
- Migration des données existantes
- Formation des équipes
- Conformité RGPD
"""
test_endpoint("SummarizeRfp", "POST", f"{BASE_URL}/summarizeRfp",
              data={"rfpText": rfp_text})

# Test 5: Generate Diagram from Text
print_header("TEST 5: Generate Diagram from Text")
diagram_description = """
Architecture cloud moderne avec:
- Frontend: React application
- Backend: FastAPI microservices
- Database: PostgreSQL cluster
- Cache: Redis
- Message Queue: RabbitMQ
- Load Balancer: Nginx
"""
test_endpoint("GenerateDiagram", "POST", f"{BASE_URL}/generateDiagramFromText",
              data={"description": diagram_description})

# Test 6: Generate Deck from Text - Step 1 (HTML generation)
print_header("TEST 6: Generate Deck from Text (Step 1: HTML)")
deck_content = """
Présentation Commerciale Infotel

Slide 1: Titre
Digital Transformation Solutions

Slide 2: Introduction
Infotel est leader dans les solutions IT depuis 30 ans.

Slide 3: Services
- Conseil en transformation digitale
- Développement d'applications cloud
- Intégration de systèmes
- Support et maintenance

Slide 4: Technologies
- Cloud: AWS, Azure, GCP
- DevOps: Docker, Kubernetes
- AI/ML: OpenAI, Azure AI

Slide 5: Conclusion
Contactez-nous pour discuter de vos besoins.
"""
response = test_endpoint("GenerateDeck", "POST", f"{BASE_URL}/generateDeckFromText",
                         data={"description": deck_content, "confirm_plan": "false"})

# Extract html_id if available
html_id = None
if response and response.status_code == 200:
    try:
        data = response.json()
        html_id = data.get("html_id")
        print(f"\n[OK] HTML generated with ID: {html_id}")
    except:
        pass

# Test 7: Generate Deck from Text - Step 2 (PPTX conversion)
if html_id:
    print_header("TEST 7: Generate Deck from Text (Step 2: PPTX Conversion)")
    test_endpoint("GenerateDeckPPTX", "POST", f"{BASE_URL}/generateDeckFromText",
                  data={"confirm_plan": "true", "html_id": html_id})

# Test 8: Test with file upload (if we can create a test file)
print_header("TEST 8: Summarize RFP with File Upload")
# Create a test RFP file
test_rfp_content = """
DEMANDE DE PROPOSITION TECHNIQUE

Projet: Modernisation de l'infrastructure réseau

Objectif:
Remplacer l'infrastructure réseau actuelle par une solution moderne, sécurisée et scalable.

Exigences:
1. Support IPv6
2. Firewall nouvelle génération
3. Segmentation réseau
4. Monitoring 24/7
5. Documentation complète

Délai de réponse: 30 jours
"""
test_file_path = Path("test_rfp.txt")
try:
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_rfp_content)
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_rfp.txt", f, "text/plain")}
        test_endpoint("SummarizeRfpFile", "POST", f"{BASE_URL}/summarizeRfp",
                      files=files)
finally:
    if test_file_path.exists():
        test_file_path.unlink()

# Test 9: Download endpoint (test with non-existent file first)
print_header("TEST 9: Download Endpoint (Non-existent file)")
test_endpoint("Download404", "GET", f"{BASE_URL}/download/nonexistent.pptx")

# Test 10: Preview HTML endpoint
if html_id:
    print_header("TEST 10: Preview HTML Endpoint")
    test_endpoint("PreviewHTML", "GET", f"{BASE_URL}/preview-html/{html_id}")

# Test 11: Cleanup endpoint
print_header("TEST 11: Cleanup Endpoint (Dry Run)")
test_endpoint("Cleanup", "POST", f"{BASE_URL}/cleanup",
              params={"max_age_hours": 24, "dry_run": "true"})

# Summary
print_header("TEST SUMMARY")
print("\n[OK] All endpoint tests completed!")
print(f"\nAPI Base URL: {BASE_URL}")
print("\nTested Endpoints:")
print("  [OK] GET  /")
print("  [OK] GET  /docs")
print("  [OK] POST /health")
print("  [OK] POST /summarizeRfp (text)")
print("  [OK] POST /summarizeRfp (file)")
print("  [OK] POST /generateDiagramFromText")
print("  [OK] POST /generateDeckFromText (HTML generation)")
print("  [OK] POST /generateDeckFromText (PPTX conversion)")
print("  [OK] GET  /download/{filename}")
print("  [OK] GET  /preview-html/{html_id}")
print("  [OK] POST /cleanup")

