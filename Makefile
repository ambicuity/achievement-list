# Makefile for GitHub Achievement Badge Automation

.PHONY: help install setup test lint clean badges

help:  ## Show this help message
	@echo "🏆 GitHub Achievement Badge Automation"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install -r requirements.txt

setup:  ## Setup environment and check configuration
	@echo "🔧 Setting up GitHub Achievement environment..."
	@python scripts/badge_cli.py setup

test:  ## Test all scripts for syntax errors
	@echo "🧪 Testing scripts..."
	@python -m py_compile scripts/*.py
	@echo "✅ All scripts compile successfully!"

lint:  ## Run basic linting on Python files
	@echo "🔍 Checking Python syntax..."
	@find scripts -name "*.py" -exec python -m py_compile {} \;
	@echo "✅ Linting complete!"

clean:  ## Clean up temporary files
	@echo "🧹 Cleaning up..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

badges:  ## Check current badge progress
	@echo "📊 Checking badge progress..."
	@python scripts/badge_cli.py status

quickstart:  ## Quick start guide
	@echo "🚀 GitHub Achievement Badge Quick Start"
	@echo ""
	@echo "1. Set your GitHub token:"
	@echo "   export GITHUB_TOKEN='your_token_here'"
	@echo ""
	@echo "2. Install dependencies:"
	@echo "   make install"
	@echo ""
	@echo "3. Verify setup:"
	@echo "   make setup"
	@echo ""
	@echo "4. Get started:"
	@echo "   python scripts/badge_cli.py tips"
	@echo ""

# Quick badge earning targets
quickdraw:  ## Earn Quickdraw badge (5 minutes)
	@python scripts/badge_cli.py quickdraw

find-repos:  ## Find repositories for contributions
	@python scripts/badge_cli.py find-repos --interactive

discussions:  ## Find GitHub discussions to answer
	@python scripts/badge_cli.py discussions

coauthor:  ## Generate co-author commit message
	@python scripts/badge_cli.py coauthor

# Development targets
dev-setup:  ## Setup development environment
	pip install -r requirements.txt
	@echo "✅ Development environment ready!"

validate:  ## Validate all configuration files
	@echo "🔍 Validating configuration..."
	@python -c "import yaml; yaml.safe_load(open('.github/workflows/badge-tracker.yml'))" 2>/dev/null && echo "✅ badge-tracker.yml valid" || echo "❌ badge-tracker.yml invalid"
	@python -c "import yaml; yaml.safe_load(open('.github/workflows/quickdraw-pr.yml'))" 2>/dev/null && echo "✅ quickdraw-pr.yml valid" || echo "❌ quickdraw-pr.yml invalid"
	@echo "✅ Validation complete!"

demo:  ## Show a demo of the tools
	@echo "🎬 GitHub Achievement Badge Tools Demo"
	@echo ""
	@echo "Main CLI:"
	@python scripts/badge_cli.py --help
	@echo ""
	@echo "Available tools:"
	@ls -la scripts/
	@echo ""
	@echo "Try: make quickstart"