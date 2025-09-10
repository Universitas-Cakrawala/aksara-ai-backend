#!/bin/bash

# Build and run development environment
echo "🚀 Starting Aksara AI Backend Development Environment..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Build the image
echo "📦 Building Docker image..."
docker compose -f docker-compose.dev.yml build

# Start the application
echo "🏃 Starting application..."
docker compose -f docker-compose.dev.yml up -d

# Show logs
echo "📋 Showing application logs..."
docker compose -f docker-compose.dev.yml logs -f aksara-ai-backend-dev
