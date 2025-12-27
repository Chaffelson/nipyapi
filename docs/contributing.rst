.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Chaffelson/nipyapi/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Nipyapi could always use more documentation, whether as part of the
official Nipyapi docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Chaffelson/nipyapi/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `nipyapi` for local development.

1. Fork the `nipyapi` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:Chaffelson/nipyapi.git

3. Create and activate a Python 3.9+ virtual environment (venv or uv), then install dev extras::

    # using venv
    $ python -m venv .venv && source .venv/bin/activate
    $ cd nipyapi/
    $ make dev-install  # uses uv if available, falls back to pip

    # or using uv (faster)
    $ uv venv .venv && source .venv/bin/activate
    $ make dev-install

   **Note:** The Makefile automatically detects whether ``uv`` is available and uses it for faster installs. If not available, it falls back to ``pip``. Both work seamlessly.

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. You may want to leverage the provided Docker profiles for testing and development

 - Install the latest version of Docker
 - Use the provided Docker Compose configuration in `resources/docker/compose.yml` and run tests via Makefile::

    # generate local test certificates (run once or after cleanup)
    $ make certs

    # bring up single-user profile and wait for readiness
    $ make up NIPYAPI_PROFILE=single-user
    $ make wait-ready NIPYAPI_PROFILE=single-user
    # run tests (conftest resolves URLs, credentials, and TLS for the profile)
    $ make test
    # bring everything down when done
    $ make down


6. When you're done making changes, run the test suites for all profiles::

    # convenience shortcuts
    $ make test-all

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Common Mistakes to Avoid
------------------------

When contributing to NiPyAPI, watch out for these frequent pitfalls:

**Installation & Environment**

* **Bracket quoting in zsh**: Running ``pip install -e .[dev]`` fails in zsh due to glob expansion. Always use quotes: ``pip install -e ".[dev]"`` or use ``make dev-install``.
* **Wrong Python version**: Project supports Python 3.9-3.12. Using 3.8 (end of life) or 3.13+ (untested) may cause compatibility issues.
* **Missing virtual environment**: Always activate a virtual environment before installing dependencies to avoid polluting system Python.

**Testing**

* **Missing NIPYAPI_PROFILE**: Never run ``pytest`` without setting ``NIPYAPI_PROFILE`` environment variable. Always use ``make test NIPYAPI_PROFILE=single-user`` or equivalent.
* **Services not ready**: Never assume Docker services are immediately ready after ``make up``. Always run ``make wait-ready NIPYAPI_PROFILE=<profile>`` before testing.
* **Stale certificates**: If you encounter certificate errors, run ``make down`` then ``make certs`` to regenerate fresh certificates. Never run ``make certs`` while containers are running.

**Code Quality**

* **Modifying generated code**: Never edit files in ``nipyapi/nifi/``, ``nipyapi/registry/``, or ``nipyapi/_version.py``. These are auto-generated and your changes will be overwritten.
* **Skipping lint checks**: Always run ``make lint`` before committing. Both flake8 and pylint must pass.
* **Incorrect line length**: Project uses 100-character line limit consistently across all tools (flake8, pylint, black, isort).

**NiFi vs Registry Security Differences**

**Important:** NiFi and Registry have different security implementations in their OpenAPI specifications:

* **NiFi 2.6.0+**: Includes native security schemes (``HTTPBearerJWT``, ``CookieSecureAuthorizationBearer``) in base OpenAPI spec
* **Registry 2.6.0+**: Has NO security schemes in base OpenAPI spec - requires augmentation

**Key implications:**

* Registry augmentation scripts (``resources/client_gen/augmentations/registry_security.py``) remain necessary even though NiFi 2.6.0 has native security
* Both services use the same authentication flow: username/password → JWT token → Bearer auth
* The template (``configuration.mustache``) handles both cases via hardcoded ``bearerAuth`` fallback plus native scheme aliases
* Always use ``augmented`` variant when regenerating clients (default) to support both NiFi and Registry
* NiFi can work without augmentation using the ``base`` variant (2.6.0+), but Registry cannot

**Docker & Infrastructure**

* **Docker volume caching**: If you experience persistent issues, run ``make clean-docker`` to remove all containers and volumes, then restart the setup process.
* **Wrong profile for test**: Ensure your ``NIPYAPI_PROFILE`` matches the profile you started with ``make up``. Mixing profiles causes authentication failures.

Make Targets Quick Reference
-----------------------------

NiPyAPI uses Makefile targets as the primary automation interface. Run ``make help`` to see all available targets organized by category.

**Setup & Installation**
::

    make dev-install      # Install with dev dependencies (uses uv if available, pip otherwise)
    make docs-install     # Install documentation dependencies
    make clean            # Remove build, pyc, and temp artifacts
    make clean-all        # Nuclear clean: removes ALL including generated code

**Testing Workflow**
::

    # Basic test workflow
    make certs                              # Generate certificates (once)
    make up NIPYAPI_PROFILE=single-user     # Start Docker services
    make wait-ready NIPYAPI_PROFILE=single-user  # Wait for readiness
    make test NIPYAPI_PROFILE=single-user   # Run tests
    make down                               # Stop services

    # Shortcuts for specific profiles
    make test-su          # single-user profile
    make test-ldap        # secure-ldap profile
    make test-mtls        # secure-mtls profile

    # Comprehensive testing
    make test-all         # Run all automated profiles (single-user, ldap, mtls)
    make coverage         # Run tests with coverage report

**Code Quality**
::

    make lint             # Run flake8 + pylint (excludes generated code)
    make flake8           # Run flake8 only
    make pylint           # Run pylint only
    make pre-commit       # Run pre-commit hooks (black, isort, flake8, pylint)

Pre-commit hooks are the recommended way to ensure code quality before committing. They automatically run formatting and linting checks.

**Troubleshooting Lint Issues**

* **Import order errors**: Run ``isort nipyapi/`` to auto-fix import ordering
* **Line length errors**: Break long lines at logical points (operators, commas). Max is 100 chars.
* **Formatting errors**: Run ``black nipyapi/`` to auto-format, then re-run ``make lint``
* **Linting generated code**: Always use ``make lint`` which excludes generated code automatically

**Docker Operations**
::

    make certs            # Generate PKCS12 certificates for secure profiles
    make up NIPYAPI_PROFILE=<profile>    # Start specific profile
    make down             # Stop all Docker services
    make wait-ready NIPYAPI_PROFILE=<profile>  # Wait for services to be ready
    make clean-docker     # Comprehensive Docker cleanup

    # Available profiles: single-user, secure-ldap, secure-mtls, secure-oidc

**Build & Documentation**
::

    make dist             # Build wheel and source distribution
    make check-dist       # Validate distribution files
    make test-dist        # Test that distribution can be imported
    make docs             # Generate Sphinx documentation

**Complete Workflows**
::

    make sandbox NIPYAPI_PROFILE=single-user  # Create sandbox with sample objects
    make rebuild-all      # Comprehensive rebuild: clean → certs → APIs → clients → test → build → docs

Generated vs Maintained Code
-----------------------------

Understanding which code is generated vs maintained is crucial for contributing:

**Generated Code (DO NOT MODIFY)**

These files are automatically generated from OpenAPI specifications and should never be edited directly:

* ``nipyapi/nifi/`` - NiFi API client
* ``nipyapi/registry/`` - Registry API client
* ``nipyapi/_version.py`` - Git version via setuptools-scm

**Why this matters:**

1. Your changes will be overwritten during the next client generation
2. These files are excluded from linting (flake8, pylint, black, isort)
3. Test coverage doesn't include generated code
4. Pull requests should not modify these paths

**Maintained Code (Where to Contribute)**

Focus your contributions on these core modules:

* ``nipyapi/bulletins.py`` - Bulletin retrieval, filtering, and clearing
* ``nipyapi/canvas.py`` - Canvas management functions
* ``nipyapi/ci.py`` - CI/CD convenience functions for flow deployment
* ``nipyapi/config.py`` - Configuration and endpoints
* ``nipyapi/extensions.py`` - NiFi extensions (NAR) management
* ``nipyapi/layout.py`` - Canvas layout and component positioning
* ``nipyapi/parameters.py`` - Parameter context operations
* ``nipyapi/profiles.py`` - Profile management system
* ``nipyapi/security.py`` - Authentication and security
* ``nipyapi/system.py`` - System-level operations
* ``nipyapi/utils.py`` - Utility functions
* ``nipyapi/versioning.py`` - Version control operations
* ``tests/`` - Test suite (always add tests for new features)
* ``examples/`` - Example scripts and usage patterns
* ``docs/`` - Documentation (RST files)

**Adding New Core Modules**

When creating a new core module (e.g., ``nipyapi/mymodule.py``):

1. Add the module name to ``nipyapi/__init__.py`` in the ``__all__`` list
2. Add a description to ``docs/scripts/generate_structured_docs.py`` in ``module_descriptions``
3. Regenerate documentation with ``make docs`` to create the RST file
4. Add corresponding tests in ``tests/test_mymodule.py``

The documentation generator auto-detects modules from ``__all__`` but uses ``module_descriptions``
for human-readable descriptions. Without an entry in ``module_descriptions``, the module will
still appear in docs but with a generic description.

**Regenerating Clients**

If you need to update the generated clients (e.g., for a new NiFi version):
::

    # Set target NiFi version
    export NIFI_VERSION=2.5.0

    # Fetch and generate
    make fetch-openapi      # Fetch specs from running NiFi
    make gen-clients        # Generate Python clients

    # Test with new clients
    make test-all

**Augmentation System**

The project includes an augmentation system for fixing OpenAPI spec issues:

* Base specs: ``resources/client_gen/api_defs/nifi-<version>.json``
* Augmentations: ``resources/client_gen/augmentations/*.py``
* Augmented specs: ``resources/client_gen/api_defs/*-<version>.augmented.json``

If you find spec issues, contribute fixes to the augmentation scripts rather than modifying generated code.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should pass lint and all three profile test suites (use `make lint` and `make test-su`, `make test-ldap`, `make test-mtls`).
   Exceptions (e.g., docs-only changes) should note why profile tests were skipped.
4. Pull requests should be created against 'main' branch for new features or work with NiFi-2.x, or maint-0.x for critical patches to NiFi-1.x featuers.
