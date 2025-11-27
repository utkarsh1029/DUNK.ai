#!/bin/bash

# Simple backend startup
cd "$(dirname "$0")"

# Activate the correct venv (in DUNK.ai directory)
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Create one with: python3 -m venv .venv"
    exit 1
fi

# Set PYTHONPATH to include backend directory
export PYTHONPATH="${PWD}/backend:${PYTHONPATH}"

# Verify we can import
python -c "from dunk_ai.api.main import app" 2>/dev/null || {
    echo "❌ Cannot import dunk_ai. Check PYTHONPATH and dependencies."
    echo "   PYTHONPATH: $PYTHONPATH"
    exit 1
}

# Run uvicorn
uvicorn dunk_ai.api.main:app --reload

