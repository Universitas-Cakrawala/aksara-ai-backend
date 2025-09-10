#!/bin/bash

# Build and run production environment with all services
echo "🚀 Starting Aksara AI Backend Production Environment..."

# Create necessary directories
mkdir -p logs
mkdir -p init-scripts
mkdir -p mongo-init

# Build and start all services
echo "📦 Building and starting all services..."
docker compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Show service status
echo "📊 Service Status:"
docker compose ps

# Show logs
echo "📋 Showing application logs..."
docker compose logs -f aksara-ai-backend
