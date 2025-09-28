.PHONY: clean clean-pyc clean-build clean-act clean-docker test docs help
.DEFAULT_GOAL := help

# Default NiFi/Registry version for docker compose profiles
NIFI_VERSION ?= 2.5.0

# Python command for cross-platform compatibility
# Defaults to 'python' for conda/venv users, override with PYTHON=python3 for system installs
PYTHON ?= python

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
BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

#################################################################################
## Operational Targets ##
#################################################################################

clean: clean-build clean-pyc clean-temp ## remove all build, test, coverage and Python artifacts

clean-all: clean-build clean-pyc clean-temp openapi-clean ## nuclear clean: removes ALL artifacts including committed generated code
	@echo "=== Nuclear Clean: Removing ALL Artifacts ==="
	@echo "WARNING: This removes committed generated code (API clients, docs)!"
	# Generated API clients (committed code)
	rm -rf nipyapi/nifi/* nipyapi/registry/* || true
	# Generated documentation (committed code)
	rm -rf docs/nipyapi-docs || true
	@echo "ALL artifacts removed: build, Python, OpenAPI, committed code, test certificates."
	@echo "Use 'make openapi-generate' and 'make docs' to regenerate committed code."

clean-temp: ## remove temporary artifacts but preserve committed code
	# Coverage artifacts
	rm -rf htmlcov/ .coverage coverage.xml .pytest_cache || true
	# Documentation build artifacts
	rm -rf docs/_build/* || true
	# Temporary generation files and cache
	rm -rf resources/client_gen/_tmp/* resources/client_gen/_cache/* || true
	# Test certificates and configuration (non-committed test artifacts)
	rm -rf resources/certs/ca/ resources/certs/nifi/ resources/certs/registry/ resources/certs/client/ resources/certs/truststore/ || true
	rm -f resources/certs/certs.env resources/certs/nifi.env resources/certs/registry.env || true
	# Auto-generated version file
	rm -f nipyapi/_version.py || true

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

clean-act: ## remove act containers and volumes (fixes certificate caching issues)
	@echo "=== Cleaning act containers and volumes ==="
	@# Remove act containers
	docker ps -a --filter 'name=act-' -q | xargs -r docker rm -f || true
	@# Remove act volumes (this fixes certificate caching issues)
	docker volume ls --format '{{.Name}}' | grep -i act | xargs -r docker volume rm || true
	@echo "Act containers and volumes cleaned (certificate cache reset)"

clean-docker: clean-act ## comprehensive Docker cleanup: act + containers + volumes + networks
	@echo "=== Comprehensive Docker cleanup ==="
	@# Clean up nipyapi-specific containers
	docker ps -a --filter 'label=com.docker.compose.project=nipyapi' -q | xargs -r docker rm -f || true
	@# Clean up nipyapi networks
	docker network ls --filter 'name=nipyapi' -q | xargs -r docker network rm || true
	@# Clean up unused volumes (be careful!)
	@echo "Removing unused Docker volumes..."
	docker volume prune -f || true
	@echo "Comprehensive Docker cleanup complete"

install: clean ## install the package to the active Python's site-packages
	pip install .

dev-install: ## install dev extras for local development
	pip install -e ".[dev]"

docs-install: ## install docs extras
	pip install -e ".[docs]"

coverage: ensure-certs ## run pytest with coverage and generate report (set coverage-min=NN to enforce; requires infrastructure)
	@echo "Running coverage analysis (single-user profile)..."
	@echo "Ensuring single-user infrastructure is ready..."
	$(MAKE) up NIPYAPI_PROFILE=single-user
	$(MAKE) wait-ready NIPYAPI_PROFILE=single-user
	@echo "Running pytest with coverage..."
	NIPYAPI_PROFILE=single-user PYTHONPATH=$(PWD):$$PYTHONPATH pytest --cov=nipyapi --cov-report=term-missing --cov-report=html
	@if [ -n "$(coverage-min)" ]; then coverage report --fail-under=$(coverage-min); fi
	@echo "Coverage analysis complete. See htmlcov/index.html for detailed report."

coverage-upload: coverage ## run coverage and upload to codecov (CI only - requires CODECOV_TOKEN)
	@echo "📤 Uploading coverage to codecov..."
	@if [ -z "$$CODECOV_TOKEN" ] && [ -z "$$CI" ]; then \
		echo "ERROR: codecov upload requires CODECOV_TOKEN environment variable or CI environment"; \
		echo "💡 For local development, use 'make coverage' to view reports in htmlcov/index.html"; \
		exit 1; \
	fi
	codecov

lint: ## run all linting checks (flake8 + pylint on core nipyapi files only)
	@echo "Running flake8..."
	flake8 nipyapi/ --config=setup.cfg --exclude=nipyapi/nifi,nipyapi/registry,nipyapi/_version.py
	@echo "Running pylint..."
	pylint nipyapi/ --rcfile=pylintrc --ignore=nifi,registry,_version.py
	@echo "All linting checks passed"

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
		(echo "ERROR: Certificates missing. Run: make certs" && exit 1)

ensure-certs: ## generate certificates only if they don't already exist
	@if [ ! -f resources/certs/certs.env ]; then \
		echo "📝 Certificates not found - generating fresh certificates..."; \
		$(MAKE) certs; \
	else \
		echo "Certificates already exist - skipping generation"; \
	fi

check-infra:
	@$(DC) ps -q 2>/dev/null | grep -q . || \
		(echo "ERROR: Infrastructure not running. Run: make up NIPYAPI_PROFILE=<profile>" && exit 1)

# Infrastructure operations
certs: ## generate PKCS12 certs and env for docker profiles
	@if $(DC) ps -q 2>/dev/null | grep -q .; then \
		echo "⚠️  Active containers detected - stopping before certificate regeneration..."; \
		$(MAKE) down; \
		echo ""; \
	fi
	cd resources/certs && bash gen_certs.sh
	@echo "Fresh certificates generated - containers will use new certs on next startup"

extract-jks: ## extract PEM certificates from JKS: make extract-jks JKS_FILE=truststore.jks JKS_PASSWORD=pass OR PROPERTIES_FILE=cli.properties
	@if [ -n "$(PROPERTIES_FILE)" ]; then \
		if [ ! -f "$(PROPERTIES_FILE)" ]; then echo "ERROR: Properties file not found: $(PROPERTIES_FILE)"; exit 1; fi; \
		cd resources/certs && bash extract_jks_certs.sh --properties "$(abspath $(PROPERTIES_FILE))"; \
	elif [ -n "$(JKS_FILE)" ] && [ -n "$(JKS_PASSWORD)" ]; then \
		if [ ! -f "$(JKS_FILE)" ]; then echo "ERROR: JKS file not found: $(JKS_FILE)"; exit 1; fi; \
		cd resources/certs && bash extract_jks_certs.sh "$(abspath $(JKS_FILE))" "$(JKS_PASSWORD)"; \
	else \
		echo "ERROR: Either PROPERTIES_FILE or both JKS_FILE and JKS_PASSWORD are required"; \
		echo "Examples:"; \
		echo "  make extract-jks JKS_FILE=/path/to/truststore.jks JKS_PASSWORD=mypassword"; \
		echo "  make extract-jks PROPERTIES_FILE=/path/to/nifi-cli.properties"; \
		exit 1; \
	fi
	@echo "✅ Certificates extracted to resources/certs/extracted/"

up: ensure-certs # bring up docker profile: make up NIPYAPI_PROFILE=single-user|secure-ldap|secure-mtls|secure-oidc (uses NIFI_VERSION=$(NIFI_VERSION))
	@if [ -z "$(NIPYAPI_PROFILE)" ]; then echo "NIPYAPI_PROFILE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi
	$(DC) --profile $(NIPYAPI_PROFILE) up -d

down: ## bring down all docker services
	@echo "Bringing down Docker services (NIFI_VERSION=$(NIFI_VERSION))"
	@$(DC) --profile single-user --profile secure-ldap --profile secure-mtls --profile secure-oidc down -v --remove-orphans || true
	@echo "Verifying expected containers are stopped/removed:"
	@COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE) ps --format "table {{.Name}}\t{{.State}}" | tail -n +2 | awk '{print " - " $$1 ": " $$2}' || true

wait-ready: ## wait for readiness using profile configuration; requires NIPYAPI_PROFILE=single-user|secure-ldap|secure-mtls|secure-oidc
	@if [ -z "$(NIPYAPI_PROFILE)" ]; then echo "ERROR: NIPYAPI_PROFILE is required"; exit 1; fi
	@echo "Waiting for $(NIPYAPI_PROFILE) infrastructure to be ready..."
	@NIPYAPI_PROFILE=$(NIPYAPI_PROFILE) $(PYTHON) resources/scripts/wait_ready.py

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

test: ## run pytest with provided NIPYAPI_PROFILE; config resolved by tests/conftest.py
	@if [ -z "$(NIPYAPI_PROFILE)" ]; then echo "NIPYAPI_PROFILE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi; \
	NIPYAPI_PROFILE=$(NIPYAPI_PROFILE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

test-su: ## shortcut: NIPYAPI_PROFILE=single-user pytest
	NIPYAPI_PROFILE=single-user $(MAKE) test

test-ldap: ## shortcut: NIPYAPI_PROFILE=secure-ldap pytest
	NIPYAPI_PROFILE=secure-ldap $(MAKE) test

test-mtls: ## shortcut: NIPYAPI_PROFILE=secure-mtls pytest
	NIPYAPI_PROFILE=secure-mtls $(MAKE) test

test-oidc: check-certs ## shortcut: NIPYAPI_PROFILE=secure-oidc pytest (requires: make sandbox NIPYAPI_PROFILE=secure-oidc)
	NIPYAPI_PROFILE=secure-oidc $(MAKE) test

test-specific: ## run specific pytest with provided NIPYAPI_PROFILE and TEST_ARGS
	@if [ -z "$(NIPYAPI_PROFILE)" ]; then echo "NIPYAPI_PROFILE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi; \
	if [ -z "$(TEST_ARGS)" ]; then echo "TEST_ARGS is required (e.g., tests/test_utils.py::test_dump -v)"; exit 1; fi; \
	NIPYAPI_PROFILE=$(NIPYAPI_PROFILE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q $(TEST_ARGS)


# Build & Documentation
dist: clean ## builds source and wheel package using modern build system
	$(PYTHON) -m build

wheel: clean ## builds wheel package only
	$(PYTHON) -m build --wheel

sdist: clean ## builds source distribution only
	$(PYTHON) -m build --sdist

check-dist: dist ## validate distribution files
	$(PYTHON) -m twine check dist/*

test-dist: dist ## test that built distribution can be imported and used
	$(PYTHON) resources/scripts/test_distribution.py

docs: ## generate Sphinx HTML documentation with improved navigation
	$(PYTHON) docs/scripts/generate_structured_docs.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo ""
	@echo "Documentation built. Open: docs/_build/html/index.html"


#################################################################################
## Meta Targets ##
#################################################################################

test-all: ensure-certs ## run full e2e tests across automated profiles (requires: make certs)
	@echo "Running full e2e tests across automated profiles..."
	@for profile in single-user secure-ldap secure-mtls; do \
		echo "=== Running e2e test for profile: $$profile ==="; \
		$(MAKE) up NIPYAPI_PROFILE=$$profile && \
		$(MAKE) wait-ready NIPYAPI_PROFILE=$$profile && \
		$(MAKE) test NIPYAPI_PROFILE=$$profile; \
		test_result=$$?; \
		if [ $$test_result -ne 0 ]; then \
			echo "Tests failed for profile: $$profile"; \
			exit $$test_result; \
		fi; \
	done
	@echo "All profiles tested successfully"

sandbox: ensure-certs ## create isolated environment with sample objects: make sandbox NIPYAPI_PROFILE=single-user|secure-ldap|secure-mtls|secure-oidc
	@if [ -z "$(NIPYAPI_PROFILE)" ]; then echo "ERROR: NIPYAPI_PROFILE is required (single-user|secure-ldap|secure-mtls|secure-oidc)"; exit 1; fi
	@echo "🏗️ Setting up NiPyAPI sandbox with profile: $(NIPYAPI_PROFILE)"
	@echo "=== 1/4: Starting infrastructure ==="
	$(MAKE) up NIPYAPI_PROFILE=$(NIPYAPI_PROFILE)
	@echo "=== 2/4: Waiting for readiness ==="
	$(MAKE) wait-ready NIPYAPI_PROFILE=$(NIPYAPI_PROFILE)
	@echo "=== 3/4: Setting up authentication and sample objects ==="
	@NIPYAPI_PROFILE=$(NIPYAPI_PROFILE) $(PYTHON) examples/sandbox.py $(NIPYAPI_PROFILE)

rebuild-all: ## comprehensive rebuild: clean -> certs -> extract APIs -> gen clients -> test all -> build -> validate -> docs
	@echo "Starting comprehensive rebuild from clean slate..."
	@echo "=== 1/9: Clean All Artifacts ==="
	$(MAKE) clean-all
	@echo "=== 2/9: Generate Certificates ==="
	$(MAKE) certs
	@echo "=== 3/9: Extract OpenAPI Specs ==="
	$(MAKE) up NIPYAPI_PROFILE=single-user
	$(MAKE) wait-ready NIPYAPI_PROFILE=single-user
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
	@echo "Comprehensive rebuild completed successfully!"
