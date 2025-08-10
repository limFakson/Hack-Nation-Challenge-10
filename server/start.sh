#!/bin/bash
set -e  # Stop on first error

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔍 Fetching Prisma binary..."
prisma py fetch

echo "⚙️ Generating Prisma client..."
prisma generate

echo "🚀 Starting FastAPI server..."
uvicorn server.server:app --host 0.0.0.0 --port 8000