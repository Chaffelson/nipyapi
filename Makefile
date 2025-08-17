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

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

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
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# remove test and coverage artifacts handled by coverage target

lint: ## run flake8 and pylint
	$(MAKE) lint-flake8
	$(MAKE) lint-pylint

lint-flake8: ## run flake8
	flake8 nipyapi tests

lint-pylint: ## run pylint
	pylint nipyapi --rcfile=pylintrc || true

test: ## run tests quickly with the default Python (env handled by tests/conftest.py)
	NIPYAPI_AUTH_MODE=single-user PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

dev-install: ## install dev extras for local development
	pip install -e ".[dev]"

docs-install: ## install docs extras
	pip install -e ".[docs]"

certs: ## generate PKCS12 certs and env for docker profiles
	cd resources/certs && bash gen_certs.sh

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
	@echo "Augmented specs refreshed."

fetch-openapi: fetch-openapi-base augment-openapi ## convenience: fetch base then augment

openapi-clean: ## remove generated augmented/backup OpenAPI artifacts
	rm -f resources/client_gen/api_defs/*.augmented.json \
	      resources/client_gen/api_defs/*.normalized.backup.json
	@echo "Cleaned generated OpenAPI artifacts."

gen-clients: ## generate NiFi and Registry clients from specs (use wv_spec_variant=augmented|base)
	cd resources/client_gen && wv_spec_variant=$${wv_spec_variant:-augmented} wv_client_name=all wv_api_def_dir=$$(pwd)/api_defs wv_tmp_dir=$$(pwd)/_tmp bash ./generate_api_client.sh

up: ## bring up docker profile: make up NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls (uses NIFI_VERSION=$(NIFI_VERSION))
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required"; exit 1; fi
	@$(DC) --profile $(NIPYAPI_AUTH_MODE) up -d

down: ## bring down all docker services
	@echo "Bringing down Docker services (NIFI_VERSION=$(NIFI_VERSION))"
	@$(DC) --profile single-user --profile secure-ldap --profile secure-mtls down -v --remove-orphans || true
	@echo "Verifying expected containers are stopped/removed:"
	@COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE) ps --format "table {{.Name}}\t{{.State}}" | tail -n +2 | awk '{print " - " $$1 ": " $$2}' || true

wait-ready: ## wait for readiness; accepts NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls or explicit *_API_ENDPOINT envs
	@# If NIPYAPI_AUTH_MODE is provided, set sensible defaults for endpoints (standardized names)
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
		else echo "Unknown NIPYAPI_AUTH_MODE $(NIPYAPI_AUTH_MODE)"; exit 1; fi; \
	fi; \
	python resources/scripts/wait_ready.py

test-profile: ## run pytest with provided NIPYAPI_AUTH_MODE; config resolved by tests/conftest.py
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls)"; exit 1; fi; \
	NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

test-su: ## shortcut: NIPYAPI_AUTH_MODE=single-user pytest
	NIPYAPI_AUTH_MODE=single-user $(MAKE) test-profile

test-ldap: ## shortcut: NIPYAPI_AUTH_MODE=secure-ldap pytest
	NIPYAPI_AUTH_MODE=secure-ldap $(MAKE) test-profile

test-mtls: ## shortcut: NIPYAPI_AUTH_MODE=secure-mtls pytest
	NIPYAPI_AUTH_MODE=secure-mtls $(MAKE) test-profile

test-specific: ## run specific pytest with provided NIPYAPI_AUTH_MODE and TEST_ARGS
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required (single-user|secure-ldap|secure-mtls)"; exit 1; fi; \
	if [ -z "$(TEST_ARGS)" ]; then echo "TEST_ARGS is required (e.g., tests/test_utils.py::test_dump -v)"; exit 1; fi; \
	NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q $(TEST_ARGS)

# Integration testing workflow (requires Docker infrastructure):
# 1. make certs
# 2. make up NIPYAPI_AUTH_MODE=single-user  
# 3. make wait-ready NIPYAPI_AUTH_MODE=single-user
# 4. make test-specific NIPYAPI_AUTH_MODE=single-user TEST_ARGS="tests/test_utils.py::test_dump -v"
# 5. make down
# Note: CI runs full integration tests with Docker infrastructure using single-user profile

test-all: ## run full e2e tests across all profiles: single-user, secure-ldap, secure-mtls
	@echo "Running full e2e tests across all profiles..."
	$(MAKE) certs
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
	@echo "All profile e2e tests completed successfully."

rebuild-all: ## comprehensive rebuild: clean -> certs -> extract APIs -> gen clients -> test all -> build -> docs
	@echo "🚀 Starting comprehensive rebuild from clean slate..."
	@echo "=== 1/8: Clean All Artifacts ==="
	$(MAKE) clean-all
	@echo "=== 2/8: Generate Certificates ==="
	$(MAKE) certs
	@echo "=== 3/8: Extract OpenAPI Specs ==="
	$(MAKE) up NIPYAPI_AUTH_MODE=single-user
	$(MAKE) wait-ready NIPYAPI_AUTH_MODE=single-user
	$(MAKE) fetch-openapi
	@echo "=== 4/8: Augment OpenAPI Specs ==="
	$(MAKE) augment-openapi
	@echo "=== 5/8: Generate Fresh Clients ==="
	$(MAKE) gen-clients
	@echo "=== 6/8: Test All Profiles with Fresh Clients ==="
	$(MAKE) test-all
	@echo "=== 7/8: Build Distribution Packages ==="
	$(MAKE) dist
	@echo "=== 8/8: Generate Documentation ==="
	$(MAKE) docs
	@echo "✅ Comprehensive rebuild completed successfully!"
	@echo "📦 Distribution: dist/"
	@echo "📚 Documentation: docs/_build/html/"

smoke: ## quick version probe without bootstrap (use NIPYAPI_AUTH_MODE=single-user|secure-ldap|secure-mtls)
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required"; exit 1; fi; \
	if [ "$(NIPYAPI_AUTH_MODE)" = "single-user" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9443/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-http://localhost:18080/nifi-registry-api}; \
		NIFI_USERNAME=$${NIFI_USERNAME:-einstein}; \
		NIFI_PASSWORD=$${NIFI_PASSWORD:-password1234}; \
		REGISTRY_USERNAME=$${REGISTRY_USERNAME:-einstein}; \
		REGISTRY_PASSWORD=$${REGISTRY_PASSWORD:-password}; \
	elif [ "$(NIPYAPI_AUTH_MODE)" = "secure-ldap" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9444/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-https://localhost:18444/nifi-registry-api}; \
		NIFI_USERNAME=$${NIFI_USERNAME:-einstein}; \
		NIFI_PASSWORD=$${NIFI_PASSWORD:-password}; \
		REGISTRY_USERNAME=$${REGISTRY_USERNAME:-einstein}; \
		REGISTRY_PASSWORD=$${REGISTRY_PASSWORD:-password}; \
	elif [ "$(NIPYAPI_AUTH_MODE)" = "secure-mtls" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9445/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-https://localhost:18445/nifi-registry-api}; \
	else echo "Unknown NIPYAPI_AUTH_MODE $(NIPYAPI_AUTH_MODE)"; exit 1; fi; \
	TLS_CA_CERT_PATH=$${TLS_CA_CERT_PATH:-$(PWD)/resources/certs/client/ca.pem}; \
	export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT NIFI_USERNAME NIFI_PASSWORD REGISTRY_USERNAME REGISTRY_PASSWORD TLS_CA_CERT_PATH; \
	python resources/scripts/smoke_versions.py

e2e: ## end-to-end: up -> wait-ready -> fetch-openapi -> augment-openapi -> gen-clients -> tests
	@if [ -z "$(NIPYAPI_AUTH_MODE)" ]; then echo "NIPYAPI_AUTH_MODE is required"; exit 1; fi; \
	$(MAKE) certs && \
	$(MAKE) up NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) && \
	$(MAKE) wait-ready NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE) && \
	$(MAKE) fetch-openapi && \
	$(MAKE) augment-openapi && \
	$(MAKE) gen-clients && \
	$(MAKE) test-profile NIPYAPI_AUTH_MODE=$(NIPYAPI_AUTH_MODE)

# tox deprecated: use Makefile targets or CI matrix

coverage-min ?= 70
coverage: ## run pytest with coverage and generate report (set coverage-min=NN to enforce)
	NIPYAPI_AUTH_MODE=single-user PYTHONPATH=$(PWD):$$PYTHONPATH pytest --cov=nipyapi --cov-report=term-missing --cov-report=xml --cov-report=html --cov-fail-under=$(coverage-min)
	$(BROWSER) htmlcov/index.html

coverage-upload: coverage ## run coverage and upload to codecov
	codecov --file coverage.xml

docs: ## generate Sphinx HTML documentation with improved navigation
	rm -rf docs/nipyapi-docs
	python docs/scripts/generate_structured_docs.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean dist ## package and upload a release
	twine check dist/*
	twine upload dist/*

dist: clean ## builds source and wheel package using modern build system
	python -m build
	ls -l dist

wheel: clean ## builds wheel package only
	python -m build --wheel
	ls -l dist

sdist: clean ## builds source distribution only
	python -m build --sdist
	ls -l dist

check-dist: dist ## validate distribution files
	twine check dist/*

test-dist: dist ## test that built distribution can be imported and used
	python resources/scripts/test_distribution.py

install: clean ## install the package to the active Python's site-packages
	pip install -e .
