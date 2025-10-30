# Makefile for best-in-class Python quant platform
.PHONY: help install dev-install test lint format type-check security audit clean run build docs
.DEFAULT_GOAL := help

PYTHON := python
UV := uv
RUFF := ruff
MYPY := mypy

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(UV) pip install -e .

dev-install: ## Install development dependencies
	$(UV) pip install -e ".[dev,test]"
	pre-commit install

test: ## Run test suite with coverage
	$(PYTHON) -m pytest

test-fast: ## Run tests without coverage for faster feedback
	$(PYTHON) -m pytest --no-cov -x

test-watch: ## Run tests in watch mode
	$(PYTHON) -m pytest --no-cov -f

bench: ## Run benchmark tests
	$(PYTHON) -m pytest -m benchmark --benchmark-only

lint: ## Run all linting checks
	$(RUFF) check .
	$(RUFF) format --check .

format: ## Format code with ruff
	$(RUFF) format .
	$(RUFF) check --fix .

type-check: ## Run type checking with mypy
	$(MYPY) quant

security: ## Run security checks
	bandit -r quant/ -f json -o security-report.json
	safety check

audit: ## Run dependency audit
	$(UV) pip check
	$(UV) pip list --outdated

quality: lint type-check security ## Run all quality checks

clean: ## Clean up build artifacts and cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ dist/ build/ *.egg-info/
	rm -rf .web/ .mypy_cache/ .ruff_cache/

run: ## Run the development server
	$(UV) run reflex run

build: ## Build the application for production
	$(UV) run reflex export --frontend-only

init: ## Initialize Reflex app
	$(UV) run reflex init

deps-update: ## Update all dependencies
	$(UV) pip list --outdated
	@echo "Run 'uv pip install -U package_name' to update specific packages"

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

docs: ## Generate documentation
	@echo "Documentation generation with Sphinx/MkDocs - TODO"

perf: ## Run performance profiling
	$(PYTHON) -m pytest tests/ -m benchmark --benchmark-json=benchmark.json

ci: quality test ## Run CI pipeline locally

setup-dev: dev-install pre-commit ## Setup complete development environment
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the application"

# Docker commands (for containerized deployment)
docker-build: ## Build Docker image
	docker build -t quant-platform .

docker-run: ## Run Docker container
	docker run -p 3000:3000 -p 8000:8000 quant-platform

# Database operations
db-init: ## Initialize database
	$(PYTHON) -c "from quant.data.database import Database; Database().init_db()"

db-migrate: ## Run database migrations
	@echo "Database migrations - TODO"

# Deployment commands
deploy-staging: ## Deploy to staging environment
	@echo "Staging deployment - TODO"

deploy-prod: ## Deploy to production environment
	@echo "Production deployment - TODO"