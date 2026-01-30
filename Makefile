.PHONY: install dev test clean build help demo

BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m

help: ## Show help
	@echo "$(BLUE)diko - CLI for downloading ISO images$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package
	@echo "$(BLUE)Installing diko...$(NC)"
	pip install -e .

dev: ## Install for development
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install -e ".[dev]"

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v

clean: ## Clean temporary files
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/

build: clean ## Build package
	@echo "$(BLUE)Building package...$(NC)"
	python -m build || python setup.py sdist bdist_wheel

	demo: install ## Demo
	@echo "$(BLUE)diko demo:$(NC)"
	@echo ""
	@echo "$(YELLOW)1. List distributions:$(NC)"
	diko list
	@echo ""
	@echo "$(YELLOW)2. Example download:$(NC)"
	@echo "   diko download debian-netinst"

.DEFAULT_GOAL := help