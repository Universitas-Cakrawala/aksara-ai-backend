# Makefile untuk Aksara AI Backend

.PHONY: help install migrate-up migrate-down migrate-create migrate-current migrate-history seed dev prod clean test

# Default target
help:
	@echo "🚀 Aksara AI Backend - Migration Commands"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install          Install dependencies"
	@echo ""
	@echo "🗄️  Database Migration:"
	@echo "  migrate-up       Apply all pending migrations"
	@echo "  migrate-down     Rollback to previous migration"
	@echo "  migrate-create   Create new migration (usage: make migrate-create MSG='description')"
	@echo "  migrate-current  Show current migration status"
	@echo "  migrate-history  Show migration history"
	@echo "  validate         Validate database setup"
	@echo ""
	@echo "🌱 Data Management:"
	@echo "  seed             Seed database with initial data"
	@echo ""
	@echo "🔧 Development:"
	@echo "  dev              Run development server"
	@echo "  prod             Run production server"
	@echo "  test             Run tests"
	@echo "  clean            Clean cache files"

# Installation
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Migration commands
migrate-up:
	@echo "⬆️  Applying migrations..."
	python migrate.py upgrade
	@echo "✅ Migrations applied!"

migrate-down:
	@echo "⬇️  Rolling back migration..."
	@if [ -z "$(REV)" ]; then \
		echo "❌ Please specify revision: make migrate-down REV=001_initial"; \
	else \
		python migrate.py downgrade $(REV); \
		echo "✅ Migration rolled back to $(REV)!"; \
	fi

migrate-create:
	@echo "📝 Creating new migration..."
	@if [ -z "$(MSG)" ]; then \
		echo "❌ Please provide message: make migrate-create MSG='Add new table'"; \
	else \
		python migrate.py create "$(MSG)"; \
		echo "✅ Migration created: $(MSG)"; \
	fi

migrate-current:
	@echo "📊 Current migration status:"
	python migrate.py current

migrate-history:
	@echo "📚 Migration history:"
	python migrate.py history

# Data seeding
seed:
	@echo "🌱 Seeding database..."
	python seed.py
	@echo "✅ Database seeded!"

# Validation
validate:
	@echo "🔍 Validating database setup..."
	python validate.py

# Development commands
dev:
	@echo "🔥 Starting development server..."
	python main.py

prod:
	@echo "🚀 Starting production server..."
	ENVIRONMENT=prod uvicorn main:app --host 0.0.0.0 --port 8000

# Testing
test:
	@echo "🧪 Running tests..."
	@echo "⚠️  No test framework configured yet"

# Utilities
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "✅ Cache files cleaned!"

# Docker commands (if using Docker)
docker-build:
	@echo "🐳 Building Docker image..."
	docker-compose -f docker-compose.yml build

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose -f docker-compose.yml up -d

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose -f docker-compose.yml down

docker-dev:
	@echo "🐳 Starting Docker development environment..."
	docker-compose -f docker-compose.dev.yml up -d

# Full setup for new environment
setup: install migrate-up seed validate
	@echo "🎉 Setup completed!"
	@echo ""
	@echo "📋 Default credentials:"
	@echo "   Username: admin"
	@echo "   Password: admin123"
	@echo ""
	@echo "🚀 Run 'make dev' to start development server"

# Database reset (be careful!)
reset-db:
	@echo "⚠️  WARNING: This will reset the entire database!"
	@echo "Press Ctrl+C to cancel, or Enter to continue..."
	@read confirm
	python migrate.py downgrade base
	python migrate.py upgrade
	python seed.py
	@echo "✅ Database reset completed!"
