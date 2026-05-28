#!/bin/bash
# Startup script for AI Disease Detection System

cd "$(dirname "$0")"

echo "Starting AI Disease Detection & Prescription System..."
echo "Project Directory: $(pwd)"
echo ""

# Activate virtual environment
source venv/bin/activate

# Set Python path
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Start Flask server
echo "Starting Flask backend server on http://localhost:5000"
python backend/app.py
