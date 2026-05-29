#!/bin/bash

# Simple frontend startup
cd "$(dirname "$0")/frontend" || {
    echo "❌ Frontend directory not found"
    exit 1
}

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🚀 Starting DUNK.ai Frontend..."
echo "📍 The server will show the URL when ready (usually http://localhost:5173)"
echo ""

# Run dev server (this will show the actual URL)
npm run dev
