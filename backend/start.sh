#!/bin/bash

echo "========================================"
echo "  Infotel RFP Summarizer Backend"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo ""
    echo "Please create a .env file with your API keys."
    echo "You can copy env_template.txt to .env and edit it."
    echo ""
    exit 1
fi

echo "Starting server on http://localhost:3001..."
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python main.py

