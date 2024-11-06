PY_PACKAGE := pokeapi
PY_PATHS := src/$(PY_PACKAGE) tests

.DEFAULT_GOAL := help

.PHONY: help
help: ## Print this help message
	@printf 'Usage: make <command>\n\nCommands:\n'
	@grep -hE '^[a-zA-Z0-9_-]+:+(.*?##.*| [\$$a-zA-Z0-9].*)?$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":+([^#]*)(##)?"}; {printf "    \033[36m%-30s\033[0m %s\n", $$1, $$2}'

init:: ## Initialize environment for running the targets in this Makefile
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

debug:: ## Print Python environment via pipenv
	pipenv graph

lint-fix:: ## Format all Python files
	pipenv run yapf --in-place --parallel --recursive --verbose $(PY_PATHS) setup.py

lint-flake8:: ## Lint via flake8
	pipenv run flake8

lint-python-style:: ## Lint via yapf
	# Fail if yapf formatter needs to reformat code
	pipenv run yapf --diff --recursive $(PY_PATHS) setup.py

lint:: lint-flake8 lint-python-style ## Run all linting

test:: ## Run tests
	pipenv run pytest --cov=$(PY_PACKAGE)

test-parallel:: ## Run tests in parallel (used by CI)
	pipenv run pytest -n 8 --forked --cov=$(PY_PACKAGE) --cov-report=xml --junit-xml=report.xml

check: init lint test ## Initialize, lint, and test

ci: lint test-parallel ## Run all CI targets

install: ## Install package locally
	pip install --editable .
