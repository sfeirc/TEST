#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test to verify AI functionality with Azure OpenAI
"""

import requests
import json
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://test-production-a01e.up.railway.app"

print("="*70)
print("Testing AI Functionality with Azure OpenAI")
print("="*70)

# Test 1: Quick RFP Summary
print("\n[TEST 1] Testing RFP Summarization...")
rfp_text = "Appel d'offres pour services cloud. Budget: 100K€. Délai: 30 jours. Technologies: AWS, Kubernetes."
response = requests.post(
    f"{BASE_URL}/summarizeRfp",
    data={"rfpText": rfp_text},
    timeout=60
)
if response.status_code == 200:
    data = response.json()
    print(f"[OK] SUCCESS: RFP analyzed")
    print(f"   Client: {data.get('identification_marche', {}).get('client_emetteur', 'N/A')}")
    print(f"   Object: {data.get('identification_marche', {}).get('objet_consultation', 'N/A')[:50]}...")
else:
    print(f"❌ FAILED: {response.status_code} - {response.text[:200]}")

# Test 2: Quick Diagram Generation
print("\n[TEST 2] Testing Diagram Generation...")
diagram_desc = "Architecture simple: Frontend React, Backend API, Database PostgreSQL"
response = requests.post(
    f"{BASE_URL}/generateDiagramFromText",
    data={"description": diagram_desc},
    timeout=60
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS: Diagram generated")
    print(f"   Title: {data.get('title', 'N/A')}")
    print(f"   Type: {data.get('type', 'N/A')}")
    print(f"   Nodes: {len(data.get('nodes', []))}")
else:
    print(f"❌ FAILED: {response.status_code} - {response.text[:200]}")

# Test 3: Quick Deck Generation (HTML)
print("\n[TEST 3] Testing Deck Generation (HTML)...")
deck_content = "Présentation Infotel: Transformation digitale, Cloud, IA, DevOps"
response = requests.post(
    f"{BASE_URL}/generateDeckFromText",
    data={"description": deck_content, "confirm_plan": "false"},
    timeout=90
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS: Deck HTML generated")
    print(f"   Title: {data.get('title', 'N/A')}")
    print(f"   Status: {data.get('status', 'N/A')}")
    print(f"   HTML ID: {data.get('html_id', 'N/A')}")
else:
    print(f"❌ FAILED: {response.status_code} - {response.text[:200]}")

print("\n" + "="*70)
print("[OK] All AI functionality tests completed!")
print("="*70)

