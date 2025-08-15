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
	pytest -q

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

up: ## bring up docker profile: make up PROFILE=single-user|secure-ldap|secure-mtls (uses NIFI_VERSION=$(NIFI_VERSION))
	@if [ -z "$(PROFILE)" ]; then echo "PROFILE is required"; exit 1; fi
	@$(DC) --profile $(PROFILE) up -d

down: ## bring down all docker services
	@echo "Bringing down Docker services (NIFI_VERSION=$(NIFI_VERSION))"
	@$(DC) --profile single-user --profile secure-ldap --profile secure-mtls down -v --remove-orphans || true
	@echo "Verifying expected containers are stopped/removed:"
	@COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE) ps --format "table {{.Name}}\t{{.State}}" | tail -n +2 | awk '{print " - " $$1 ": " $$2}' || true

wait-ready: ## wait for readiness; accepts PROFILE=single-user|secure-ldap|secure-mtls or explicit *_API_ENDPOINT envs
	@# If PROFILE is provided, set sensible defaults for endpoints (standardized names)
	@if [ -n "$(PROFILE)" ]; then \
		if [ "$(PROFILE)" = "single-user" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9443/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-http://localhost:18080/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		elif [ "$(PROFILE)" = "secure-ldap" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9444/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-https://localhost:18444/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		elif [ "$(PROFILE)" = "secure-mtls" ]; then \
			NIFI_API_ENDPOINT="$${NIFI_API_ENDPOINT:-https://localhost:9445/nifi-api}"; \
			REGISTRY_API_ENDPOINT="$${REGISTRY_API_ENDPOINT:-https://localhost:18445/nifi-registry-api}"; \
			export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT; \
		else echo "Unknown PROFILE $(PROFILE)"; exit 1; fi; \
	fi; \
	python resources/scripts/wait_ready.py

test-profile: ## run pytest with provided PROFILE; config resolved by tests/conftest.py
	@if [ -z "$(PROFILE)" ]; then echo "PROFILE is required (single-user|secure-ldap|secure-mtls)"; exit 1; fi; \
	PROFILE=$(PROFILE) PYTHONPATH=$(PWD):$$PYTHONPATH pytest -q

test-su: ## shortcut: PROFILE=single-user pytest
	PROFILE=single-user $(MAKE) test-profile

test-ldap: ## shortcut: PROFILE=secure-ldap pytest
	PROFILE=secure-ldap $(MAKE) test-profile

test-mtls: ## shortcut: PROFILE=secure-mtls pytest
	PROFILE=secure-mtls $(MAKE) test-profile

test-all: ## run full e2e tests across all profiles: single-user, secure-ldap, secure-mtls
	@echo "Running full e2e tests across all profiles..."
	$(MAKE) certs
	@for profile in single-user secure-ldap secure-mtls; do \
		echo "=== Running e2e test for profile: $$profile ==="; \
		$(MAKE) up PROFILE=$$profile && \
		$(MAKE) wait-ready PROFILE=$$profile && \
		$(MAKE) test-profile PROFILE=$$profile; \
		test_result=$$?; \
		echo "=== Cleaning up profile: $$profile ==="; \
		$(MAKE) down; \
		if [ $$test_result -ne 0 ]; then \
			echo "Tests failed for profile: $$profile"; \
			exit $$test_result; \
		fi; \
	done
	@echo "All profile e2e tests completed successfully."

smoke: ## quick version probe without bootstrap (use PROFILE=single-user|secure-ldap|secure-mtls)
	@if [ -z "$(PROFILE)" ]; then echo "PROFILE is required"; exit 1; fi; \
	if [ "$(PROFILE)" = "single-user" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9443/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-http://localhost:18080/nifi-registry-api}; \
		NIFI_USERNAME=$${NIFI_USERNAME:-einstein}; \
		NIFI_PASSWORD=$${NIFI_PASSWORD:-password1234}; \
		REGISTRY_USERNAME=$${REGISTRY_USERNAME:-einstein}; \
		REGISTRY_PASSWORD=$${REGISTRY_PASSWORD:-password}; \
	elif [ "$(PROFILE)" = "secure-ldap" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9444/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-https://localhost:18444/nifi-registry-api}; \
		NIFI_USERNAME=$${NIFI_USERNAME:-einstein}; \
		NIFI_PASSWORD=$${NIFI_PASSWORD:-password}; \
		REGISTRY_USERNAME=$${REGISTRY_USERNAME:-einstein}; \
		REGISTRY_PASSWORD=$${REGISTRY_PASSWORD:-password}; \
	elif [ "$(PROFILE)" = "secure-mtls" ]; then \
		NIFI_API_ENDPOINT=$${NIFI_API_ENDPOINT:-https://localhost:9445/nifi-api}; \
		REGISTRY_API_ENDPOINT=$${REGISTRY_API_ENDPOINT:-https://localhost:18445/nifi-registry-api}; \
	else echo "Unknown PROFILE $(PROFILE)"; exit 1; fi; \
	TLS_CA_CERT_PATH=$${TLS_CA_CERT_PATH:-$(PWD)/resources/certs/client/ca.pem}; \
	export NIFI_API_ENDPOINT REGISTRY_API_ENDPOINT NIFI_USERNAME NIFI_PASSWORD REGISTRY_USERNAME REGISTRY_PASSWORD TLS_CA_CERT_PATH; \
	python resources/scripts/smoke_versions.py

e2e: ## end-to-end: up -> wait-ready -> fetch-openapi -> augment-openapi -> gen-clients -> tests
	@if [ -z "$(PROFILE)" ]; then echo "PROFILE is required"; exit 1; fi; \
	$(MAKE) certs && \
	$(MAKE) up PROFILE=$(PROFILE) && \
	$(MAKE) wait-ready PROFILE=$(PROFILE) && \
	$(MAKE) fetch-openapi && \
	$(MAKE) augment-openapi && \
	$(MAKE) gen-clients && \
	$(MAKE) test-profile PROFILE=$(PROFILE)

# tox deprecated: use Makefile targets or CI matrix

coverage-min ?= 70
coverage: ## run pytest with coverage and generate report (set coverage-min=NN to enforce)
	coverage run --source nipyapi -m pytest
	coverage report -m --fail-under=$(coverage-min)
	coverage xml -o coverage.xml
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/nipyapi.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ nipyapi
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
