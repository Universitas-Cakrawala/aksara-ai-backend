#!/bin/bash

echo "🛑 Stopping Aksara AI Backend services..."

# Stop development environment
if [ "$1" == "dev" ]; then
    echo "Stopping development environment..."
    docker compose -f docker-compose.dev.yml down
elif [ "$1" == "prod" ]; then
    echo "Stopping production environment..."
    docker compose down
elif [ "$1" == "all" ]; then
    echo "Stopping all environments..."
    docker compose -f docker-compose.dev.yml down
    docker compose down
    
    # Clean up volumes if requested
    if [ "$2" == "clean" ]; then
        echo "🧹 Cleaning up volumes..."
        docker volume prune -f
        docker system prune -f
    fi
else
    echo "Usage: ./stop.sh [dev|prod|all] [clean]"
    echo "  dev   - Stop development environment"
    echo "  prod  - Stop production environment" 
    echo "  all   - Stop all environments"
    echo "  clean - Also remove volumes and unused containers (use with 'all')"
fi

echo "✅ Services stopped."
