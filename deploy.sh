#!/bin/bash

# InterviewAI Deployment Script
# This script helps deploy the InterviewAI application to production

set -e

echo "🚀 Starting InterviewAI deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production file not found. Please create it from .env.production.example"
    exit 1
fi

# Load environment variables
source .env.production

# Validate required environment variables
required_vars=("OPENAI_API_KEY" "JWT_SECRET_KEY" "MONGO_ROOT_USERNAME" "MONGO_ROOT_PASSWORD")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Environment variable $var is not set in .env.production"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Create necessary directories
mkdir -p nginx/ssl
mkdir -p uploads

# Check if SSL certificates exist
if [ ! -f nginx/ssl/cert.pem ] || [ ! -f nginx/ssl/key.pem ]; then
    echo "⚠️ SSL certificates not found. Generating self-signed certificates..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/key.pem \
        -out nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "⚠️ Self-signed certificates generated. For production, use proper SSL certificates."
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Pull latest images
echo "📥 Pulling latest images..."
docker-compose -f docker-compose.prod.yml pull

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

if curl -f http://localhost/api/v1/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Show running containers
echo "📋 Running containers:"
docker-compose -f docker-compose.prod.yml ps

echo "🎉 Deployment completed successfully!"
echo "🌐 Application is available at: https://localhost"
echo "📊 Admin panel: https://localhost/admin"
echo "🔧 API documentation: https://localhost/docs"

# Show logs for troubleshooting
echo "📝 To view logs, run:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"

echo "💡 To stop the application, run:"
echo "   docker-compose -f docker-compose.prod.yml down"
