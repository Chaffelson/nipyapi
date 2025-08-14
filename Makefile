.PHONY: clean clean-pyc clean-build docs help
.DEFAULT_GOAL := help

# Default NiFi/Registry version for docker compose profiles
NIFI_VERSION ?= 2.5.0

# Paths and docker compose helpers (avoid cd by using -f)
COMPOSE_DIR := $(abspath resources/docker)
COMPOSE_FILE := $(COMPOSE_DIR)/compose.yml
DC := NIFI_VERSION=$(NIFI_VERSION) docker compose -f $(COMPOSE_FILE)
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
	@echo " - Bringing down profile: single-user" && $(DC) --profile single-user down -v || true
	@echo " - Bringing down profile: secure-ldap" && $(DC) --profile secure-ldap down -v || true
	@echo " - Bringing down profile: secure-mtls" && $(DC) --profile secure-mtls down -v || true
	@echo " - Ensuring project is fully down" && $(DC) down -v || true
	@echo "Verifying expected containers are stopped/removed:"
	@expect_names="nifi-single registry-single nifi-ldap registry-ldap nifi-mtls registry-mtls"; \
	for n in $$expect_names; do \
		if docker ps -a --format '{{.Names}}' | grep -Fxq "$$n"; then \
			echo " - $$n: STILL PRESENT"; \
		else \
			echo " - $$n: not present"; \
		fi; \
	done

wait-ready: ## wait for readiness; accepts PROFILE=single-user|secure-ldap|secure-mtls or explicit *BASE_URL envs
	@# If PROFILE is provided, set sensible defaults for URLs
	@if [ -n "$(PROFILE)" ]; then \
		if [ "$(PROFILE)" = "single-user" ]; then \
			NIFI_BASE_URL="$${NIFI_BASE_URL:-https://localhost:9443/nifi-api}"; \
			REGISTRY_BASE_URL="$${REGISTRY_BASE_URL:-http://localhost:18080/nifi-registry-api}"; \
			export NIFI_BASE_URL REGISTRY_BASE_URL; \
		elif [ "$(PROFILE)" = "secure-ldap" ]; then \
		NIFI_BASE_URL="$${NIFI_BASE_URL:-https://localhost:9444/nifi-api}"; \
		REGISTRY_BASE_URL="$${REGISTRY_BASE_URL:-https://localhost:18444/nifi-registry-api}"; \
			export NIFI_BASE_URL REGISTRY_BASE_URL; \
		elif [ "$(PROFILE)" = "secure-mtls" ]; then \
		NIFI_BASE_URL="$${NIFI_BASE_URL:-https://localhost:9445/nifi-api}"; \
		REGISTRY_BASE_URL="$${REGISTRY_BASE_URL:-https://localhost:18445/nifi-registry-api}"; \
			export NIFI_BASE_URL REGISTRY_BASE_URL; \
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

e2e: ## end-to-end: up -> wait-ready -> fetch-openapi -> augment-openapi -> gen-clients -> tests
	@if [ -z "$(PROFILE)" ]; then echo "PROFILE is required"; exit 1; fi; \
	$(MAKE) certs && \
	$(MAKE) up PROFILE=$(PROFILE) && \
	$(MAKE) wait-ready PROFILE=$(PROFILE) && \
	$(MAKE) fetch-openapi && \
	$(MAKE) augment-openapi && \
	$(MAKE) gen-clients && \
	$(MAKE) test-profile PROFILE=$(PROFILE)


# Deprecated tox target
test-all: ## (deprecated) use GitHub Actions matrix or run make test locally
	@echo "Deprecated: use PROFILE=... make test or CI matrix instead."

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


servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
