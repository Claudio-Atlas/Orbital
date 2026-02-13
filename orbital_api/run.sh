#!/bin/bash
# Start the Orbital Solver API

cd "$(dirname "$0")"

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Check for required keys
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   Create .env file with your API key (see .env.example)"
    exit 1
fi

echo "🚀 Starting Orbital Solver API..."
echo "   Docs: http://localhost:8000/docs"
echo ""

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
