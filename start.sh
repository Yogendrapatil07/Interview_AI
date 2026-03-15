#!/bin/bash

echo "🚀 Starting InterviewAI..."
echo

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    echo
    echo "Option 1: Install Docker from https://docker.com"
    echo "Option 2: Run manual setup (see QUICK_START.md)"
    exit 1
fi

echo "✅ Docker found"
echo

# Check if environment files exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo
    echo "⚠️  Please edit .env file with your OpenAI API key"
    echo "   OPENAI_API_KEY=your_key_here"
    echo
fi

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend/.env file..."
    cp frontend/.env.example frontend/.env
fi

echo "🐳 Starting services with Docker..."
echo
echo "This will take a few minutes on first run..."
echo

# Start Docker Compose
docker-compose up --build

echo
echo "🛑 Press Ctrl+C to stop all services"
echo "🌐 Access the app at http://localhost:3000"
echo "📚 API docs at http://localhost:8000/docs"
