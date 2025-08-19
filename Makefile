.PHONY: clean clean-pyc clean-build docs help
.DEFAULT_GOAL := help

# Default NiFi/Registry version for docker compose profiles
NIFI_VERSION ?= 2.5.0

# Paths and docker compose helpers (avoid cd by using -f)
COMPOSE_DIR := $(abspath resources/docker)
COMPOSE_FILE := $(COMPOSE_DIR)/compose.yml
# Use a stable project name to avoid noisy warnings about defaulting to 'docker'
COMPOSE_PROJECT_NAME ?= nipyapi
DC := COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE)

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

current_section = ""
sections = {}

for line in sys.stdin:
	# Check for section headers
	section_match = re.match(r'^## (.+) ##$$', line)
	if section_match:
		current_section = section_match.group(1)
		sections[current_section] = []
		continue
	
	# Check for targets
	target_match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if target_match:
		target, help_text = target_match.groups()
		if current_section:
			sections[current_section].append((target, help_text))

# Print sections in order
section_order = ["Operational Targets", "Low-Level Targets", "Meta Targets"]
for section in section_order:
	if section in sections:
		print(f"\n{section}:")
		print("=" * (len(section) + 1))
		for target, help_text in sections[section]:
			print(f"  {target:<18} {help_text}")

# Print any remaining sections not in the predefined order
for section, targets in sections.items():
	if section not in section_order:
		print(f"\n{section}:")
		print("=" * (len(section) + 1))
		for target, help_text in targets:
			print(f"  {target:<18} {help_text}")
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

#################################################################################
## Operational Targets ##
#################################################################################

clean: clean-build clean-pyc ## remove all build, test, coverage and Python artifacts

clean-all: clean-build clean-pyc openapi-clean ## comprehensive clean: ALL artifacts (build + clients + specs + docs + coverage)
	@echo "=== Comprehensive Clean: ALL Artifacts ==="
	# Generated clients
	rm -rf nipyapi/nifi/apis/* nipyapi/nifi/models/* || true
	rm -rf nipyapi/registry/apis/* nipyapi/registry/models/* || true
	# Generated documentation
	rm -rf docs/nipyapi-docs docs/_build/* || true
	# Coverage artifacts
	rm -rf htmlcov/ .coverage coverage.xml .pytest_cache || true
	# Temporary generation files
	rm -rf resources/client_gen/_tmp/* || true
	# Auto-generated version file
	rm -f nipyapi/_version.py || true
	@echo "✅ ALL artifacts removed: build, Python, OpenAPI, clients, docs, coverage, temp files."

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

openapi-clean: ## remove generated augmented/backup OpenAPI artifacts
	rm -f resources/client_gen/api_defs/*.augmented.json \
	      resources/client_gen/api_defs/*.normalized.backup.json
	@echo "Cleaned generated OpenAPI artifacts."

install: clean ## install the package to the active Python's site-packages
	pip install .

dev-install: ## install dev extras for local development
	pip install -e ".[dev]"

docs-install: ## install docs extras
	pip install -e ".[docs]"

coverage: check-certs ## run pytest with coverage and generate report (set coverage-min=NN to enforce; requires infrastructure)
	@echo "🧪 Running coverage analysis (single-user profile)..."
	@echo "Ensuring single-user infrastructure is ready..."
	$(MAKE) up NIPYAPI_AUTH_MODE=single-user
	$(MAKE) wait-ready NIPYAPI_AUTH_MODE=single-user
	@echo "Running pytest with coverage..."
	NIPYAPI_AUTH_MODE=single-user PYTHONPATH=$(PWD):$$PYTHONPATH pytest --cov=nipyapi --cov-report=term-missing --cov-report=html
	@if [ -n "$(coverage-min)" ]; then coverage report --fail-under=$(coverage-min); fi
	@echo "✅ Coverage analysis complete. See htmlcov/index.html for detailed report."

coverage-upload: coverage ## run coverage and upload to codecov (CI only - requires CODECOV_TOKEN)
	@echo "📤 Uploading coverage to codecov..."
	@if [ -z "$$CODECOV_TOKEN" ] && [ -z "$$CI" ]; then \
		echo "❌ codecov upload requires CODECOV_TOKEN environment variable or CI environment"; \
		echo "💡 For local development, use 'make coverage' to view reports in htmlcov/index.html"; \
		exit 1; \
	fi
	codecov

lint: ## run all linting checks (flake8 + pylint on core nipyapi files only)
	@echo "Running flake8..."
	flake8 nipyapi/ --config=setup.cfg --exclude=nipyapi/nifi,nipyapi/registry,nipyapi/_version.py
	@echo "Running pylint..."
	pylint nipyapi/ --rcfile=pylintrc --ignore=nifi,registry,_version.py
	@echo "✅ All linting checks passed"

flake8: ## run flake8 linter on core nipyapi files
	flake8 nipyapi/ --config=setup.cfg --exclude=nipyapi/nifi,nipyapi/registry,nipyapi/_version.py

pylint: ## run pylint on core nipyapi files
	pylint nipyapi/ --rcfile=pylintrc --ignore=nifi,registry,_version.py

pre-commit: ## run pre-commit hooks on all files
	pre-commit run --all-files

#################################################################################
## Low-Level Targets ##
#################################################################################

# Dependency checking functions
check-certs:
	@test -f resources/certs/certs.env || \
		(echo "❌ Certificates missing. Run: make certs" && exit 1)

check-infra:
	@$(DC) ps -q 2>/dev/null | grep -q . || \
		(echo "❌ Infrastructure not running. Run: make up NIPYAPI_AUTH_MODE=<profile>" && exit 1)

# Infrastructure operations
certs: ## generate PKCS12 certs and env for docker profiles
	@if $(DC) ps -q 2>/dev/null | grep -q .; then \
		echo "⚠️  Active containers detected - stopping before certificate regeneration..."; \
		$(MAKE) down; \
		echo ""; \
	fi
	cd resources/certs && bash gen_certs.sh
	@echo "✅ Fresh certificates generated - containers will use new certs on next startup"

up: ## bring up docker profile: make up NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls|secure-oidc (uses NIFI_VERSION=$(NIFI_VERSION))
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi
	$(DC) --profile $(NIPYAPI_AUTH_MODE) up -d

down: ## bring down all docker services
	@echo "Bringing down Docker services (NIFI_VERSION=$(NIFI_VERSION))"
	@$(DC) --profile single-user --profile secure-ldap --profile secure-mtls --profile secure-oidc down -v --remove-orphans || true
	@echo "Verifying expected containers are stopped/removed:"
	@COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE) ps --format "table {{.Name}}\t{{.State}}" | tail -n +2 | awk '{print " - " $$1 ": " $$2}' || true

wait-ready: ## wait for readiness; accepts NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls|secure-oidc or explicit *_API_ENDPOINT envs
	@if [ -n "$(NIPYAPI_AUTH_MODE)" ]; then \
		if [ "$(NIPYAPI_AUTH_MODE)" = "single-user" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9443/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-http://localhost:18080/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		elif [ "$(NIPYAPI_AUTH_MODE)" = "secure-ldap" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9444/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-https://localhost:18444/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		elif [ "$(NIPYAPI_AUTH_MODE)" = "secure-mtls" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9445/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-https://localhost:18445/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		elif [ "$(NIPYAPI_AUTH_MODE)" = "secure-oidc" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9446/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-http://localhost:18446/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		else echo "Unknown NIPYAPI_AUTH_MODE $(NIPYAPI_AUTH_MODE)"; exit 1; fi; \
	fi; \
	python resources/scripts/wait_ready.py

# API & Client generation
fetch-openapi-base: ## refresh base OpenAPI specs for current NIFI_VERSION (always overwrite base)
	@echo "Refreshing base specs for NIFI_VERSION=$(NIFI_VERSION)"
	bash resources/client_gen/fetch_nifi_openapi.sh nifi-single || exit 1
	bash resources/client_gen/fetch_registry_openapi.sh registry-single || exit 1
	@echo "Base specs refreshed."

augment-openapi: ## generate augmented OpenAPI specs from base (always overwrite augmented)
	@echo "Generating augmented specs for NIFI_VERSION=$(NIFI_VERSION)"
	rm -f resources/client_gen/api_defs/nifi-$(NIFI_VERSION).augmented.json \
	      resources/client_gen/api_defs/registry-$(NIFI_VERSION).augmented.json
	bash resources/client_gen/apply_augmentations.sh nifi \
		resources/client_gen/api_defs/nifi-$(NIFI_VERSION).json \
		resources/client_gen/api_defs/nifi-$(NIFI_VERSION).augmented.json
	bash resources/client_gen/apply_augmentations.sh registry \
		resources/client_gen/api_defs/registry-$(NIFI_VERSION).json \
		resources/client_gen/api_defs/registry-$(NIFI_VERSION).augmented.json
	@echo "Augmented specs generated."

fetch-openapi: fetch-openapi-base augment-openapi ## convenience: fetch base then augment

gen-clients: ## generate NiFi and Registry clients from specs (use wv_spec_variant=augmented|base)
	WV_SPEC_VARIANT=augmented bash resources/client_gen/generate_api_client.sh

# Individual testing
test: ## run tests quickly with the default Python (env handled by tests/conftest.py)
	NIPYAPI_AUTH_MODE=single-user PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

test-profile: ## run pytest with provided NIPYAPI_AUTH_MODE; config resolved by tests/conftest.py
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi; \
	NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

test-su: ## shortcut: NIPYAPI_AUTH_MODE=single-user pytest
	NIPYAPI_AUTH_MODE=single-user $(MAKE) test-profile

test-ldap: ## shortcut: NIPYAPI_AUTH_MODE=secure-ldap pytest
	NIPYAPI_AUTH_MODE=secure-ldap $(MAKE) test-profile

test-mtls: ## shortcut: NIPYAPI_AUTH_MODE=secure-mtls pytest
	NIPYAPI_AUTH_MODE=secure-mtls $(MAKE) test-profile

test-oidc: check-certs ## shortcut: NIPYAPI_AUTH_MODE=secure-oidc pytest (requires: make sandbox NIPYAPI_AUTH_MODE=secure-oidc)
	NIPYAPI_AUTH_MODE=secure-oidc $(MAKE) test-profile

test-specific: ## run specific pytest with provided NIPYAPI_AUTH_MODE and TEST_ARGS
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi; \
	if [ -z "$(TEST_ARGS)" ]; then echo "TEST_ARGS is required (e.g., tests/test_utils.py::test_dump -v)"; exit 1; fi; \
	NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q $(TEST_ARGS)


# Build & Documentation
dist: clean ## builds source and wheel package using modern build system
	python -m build

wheel: clean ## builds wheel package only
	python -m build --wheel

sdist: clean ## builds source distribution only
	python -m build --sdist

check-dist: dist ## validate distribution files
	python -m twine check dist/*

test-dist: dist ## test that built distribution can be imported and used
	python resources/scripts/test_distribution.py

docs: ## generate Sphinx HTML documentation with improved navigation
	python docs/scripts/generate_structured_docs.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo ""
	@echo "Documentation built. Open: docs/_build/html/index.html"


#################################################################################
## Meta Targets ##
#################################################################################

test-all: check-certs ## run full e2e tests across automated profiles (requires: make certs)
	@echo "Running full e2e tests across automated profiles..."
	@for profile in single-user secure-ldap secure-mtls; do \
		echo "=== Running e2e test for profile: $$profile ==="; \
		$(MAKE) up NIPYAPI_AUTH_MODE=$$profile && \
		$(MAKE) wait-ready NIPYAPI_AUTH_MODE=$$profile && \
		$(MAKE) test-profile NIPYAPI_AUTH_MODE=$$profile; \
		test_result=$$?; \
		echo "=== Cleaning up profile: $$profile ==="; \
		$(MAKE) down; \
		if [ $$test_result -ne 0 ]; then \
			echo "Tests failed for profile: $$profile"; \
			exit $$test_result; \
		fi; \
	done
	@echo "✅ All profiles tested successfully"

sandbox: check-certs ## create isolated environment with sample objects: make sandbox NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls|secure-oidc
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "❌ NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi
	@echo "🏗️ Setting up NiPyAPI sandbox with profile: $(NIPYAPI_AUTH_MODE)"
	@echo "=== 1/4: Starting infrastructure ==="
	$(MAKE) up NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE)
	@echo "=== 2/4: Waiting for readiness ==="
	$(MAKE) wait-ready NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE)
	@echo "=== 3/4: Setting up authentication and sample objects ==="
	@NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) python examples/sandbox.py $(NIPYAPI_AUTH_MODE)

rebuild-all: ## comprehensive rebuild: clean -> certs -> extract APIs -> gen clients -> test all -> build -> validate -> docs
	@echo "🚀 Starting comprehensive rebuild from clean slate..."
	@echo "=== 1/9: Clean All Artifacts ==="
	$(MAKE) clean-all
	@echo "=== 2/9: Generate Certificates ==="
	$(MAKE) certs
	@echo "=== 3/9: Extract OpenAPI Specs ==="
	$(MAKE) up NIPYAPI_AUTH_MODE=single-user
	$(MAKE) wait-ready NIPYAPI_AUTH_MODE=single-user
	$(MAKE) fetch-openapi
	@echo "=== 4/9: Augment OpenAPI Specs ==="
	$(MAKE) augment-openapi
	@echo "=== 5/9: Generate Fresh Clients ==="
	$(MAKE) gen-clients
	@echo "=== 6/9: Test All Profiles with Fresh Clients ==="
	$(MAKE) test-all
	@echo "=== 7/9: Build Distribution Packages ==="
	$(MAKE) dist
	@echo "=== 8/9: Validate Distribution Packages ==="
	$(MAKE) check-dist
	$(MAKE) test-dist
	@echo "=== 9/9: Generate Documentation ==="
	$(MAKE) docs
	@echo "✅ Comprehensive rebuild completed successfully!"

