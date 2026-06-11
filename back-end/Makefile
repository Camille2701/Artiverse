.PHONY: install-dev test migrate format help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-dev: ## Install development dependencies
	pip install pip-tools
	pip-compile requirements/base.in
	pip-compile requirements/development.in
	pip install -r requirements/development.txt

test: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html

migrate: ## Run database migrations
	alembic upgrade head

format: ## Format code with black
	black app/ tests/

lint: ## Run linting checks
	ruff check app/ tests/
	mypy app/

dev: ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
