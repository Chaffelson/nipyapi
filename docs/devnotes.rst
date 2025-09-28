.. highlight:: shell

=================
Development Notes
=================

A collection point for information about the development process for future collaborators


Decision Points
---------------

* OpenAPI-based client generation using swagger-codegen v3 (OpenAPI 3.x definitions), with project-specific mustache templates
* We use Google style Docstrings to better enable Sphinx to produce nicely readable documentation
* We try to use minimal dependencies, and prefer to use the standard library where possible

Docker Test Environment
-----------------------

There is an Apache NiFi image available on Dockerhub::

    docker pull apache/nifi:latest

There are a couple of configuration files for launching various Docker environment configurations in resources/docker for convenience.


Testing Notes
-------------

When running tests on new code, start with the single-user profile, then test secure profiles:

.. code-block:: shell

    # Full test suite with infrastructure setup/teardown (recommended)
    make test-all

    # Manual workflow for individual profile testing:
    # 1. Set up infrastructure
    make certs
    make up NIPYAPI_PROFILE=single-user
    make wait-ready NIPYAPI_PROFILE=single-user

    # 2. Run tests (assumes infrastructure is running)
    make test NIPYAPI_PROFILE=single-user

    # 3. Clean up
    make down

    # Other profiles follow the same pattern:
    make up NIPYAPI_PROFILE=secure-ldap && make wait-ready NIPYAPI_PROFILE=secure-ldap
    make test NIPYAPI_PROFILE=secure-ldap
    make down

Because of the way errors are propagated, you may have code failures which cause a teardown that then fails because of security controls, which can obscure the original error. Starting with single-user helps isolate functional issues from authentication complexities.


Setup Code Signing
------------------

**Signed commits are required for all pull requests.** This ensures commit authenticity and maintains project security.

For OS-specific GPG setup instructions, see the `GitHub documentation on commit signature verification <https://docs.github.com/en/authentication/managing-commit-signature-verification>`_.

**Quick Setup for macOS**::

    # Install GPG via Homebrew (recommended)
    brew install gnupg

    # Generate signing keys (use a strong passphrase)
    gpg --full-generate-key

    # Configure git to use GPG signing
    git config --global user.signingkey <your-key-id>
    git config --global commit.gpgsign true

    # Add GPG TTY setting to shell profile
    echo 'export GPG_TTY=$(tty)' >> ~/.zshrc
    source ~/.zshrc

**For other operating systems:**

- **Ubuntu/Debian**: ``sudo apt install gnupg``
- **Windows**: Use Git for Windows with GPG4Win or WSL

Ensure your GPG public key is added to your GitHub account under Settings → SSH and GPG keys.


Troubleshooting Development Issues
----------------------------------

Docker and Certificate Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: SSL certificate chain errors or "authority and subject key identifier mismatch" during testing

**Cause**: Docker volume caching can serve stale certificates, especially when using ``act`` for local CI testing.

**Solution**: Clean Docker containers and volumes to force fresh certificate generation:

.. code-block:: shell

    # Quick fix for act certificate caching
    make clean-act

    # Comprehensive Docker cleanup (containers + volumes + networks)
    make clean-docker

    # Then regenerate certificates and restart testing
    make certs
    make test-mtls

**Problem**: ``act`` (GitHub Actions local runner) shows certificate errors that don't occur in local Docker testing

**Root Cause**: ``act`` maintains persistent Docker volumes between runs, which can cache stale certificates even after ``make certs`` regenerates fresh ones.

**Solution**: Always run ``make clean-act`` before testing with ``act``:

.. code-block:: shell

    # Clean act cache and test
    make clean-act
    act --job test-python-312-secure-mtls

    # Or use the comprehensive cleanup
    make clean-docker

**Problem**: Connection drops during test execution in CI environments while local testing works

**Known**: Local Docker testing works fine with same configuration. Issue appears specific to CI execution environment.

**Error Pattern**: "Connection aborted" or "Remote end closed connection without response" errors in CI (both ``act`` and GitHub Actions) while local tests pass typically indicate infrastructure/timing issues rather than configuration problems. The SSL handshake succeeds but HTTP requests return empty responses.

act (GitHub Actions Local Testing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Best Practices for act Testing**:

.. code-block:: shell

    # Always clean before testing to avoid cache issues
    make clean-act
    make clean-docker

    # Run specific job with proper platform
    act --job test-python-312-secure-mtls \
        --platform ubuntu-latest=catthehacker/ubuntu:act-latest \
        --container-architecture linux/amd64

    # Use clean flags for completely fresh environment
    act --bind --rm --job <job-name>

**Known Issues**:
- Certificate caching in Docker volumes
- Different behavior compared to real GitHub Actions (timing, resource limits)
- Docker-in-Docker networking complexities

For critical CI validation, prefer testing on actual GitHub Actions when ``act`` shows persistent issues.


Generate API Clients
---------------------

NiPyAPI uses automated client generation from OpenAPI 3.x specifications. The process is streamlined through Make targets and shell scripts in ``resources/client_gen/``.

Prerequisites
~~~~~~~~~~~~~

- Java 17+ (for swagger-codegen-cli)
- Running NiFi/Registry instances to fetch current OpenAPI specs from

Client Generation Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The complete client regeneration process:

.. code-block:: shell

    # Full regeneration (clean -> certs -> infra -> fetch specs -> generate clients)
    make rebuild-all

    # Individual steps for targeted updates:

    # 1. Start NiFi infrastructure (single-user sufficient for spec extraction)
    make certs
    make up NIPYAPI_PROFILE=single-user && make wait-ready NIPYAPI_PROFILE=single-user

    # 2. Extract OpenAPI specifications from running instances
    make fetch-openapi

    # 3. Apply authentication augmentations (temporary workaround until upstream fixes)
    make augment-openapi

    # 4. Generate Python clients using swagger-codegen + custom templates
    make gen-clients

    # 5. Test generated clients
    make test-all

    # 6. Clean up infrastructure
    make down

Customization
~~~~~~~~~~~~~

- **Templates**: Custom Mustache templates in ``resources/client_gen/swagger_templates/`` control generated code formatting
- **Augmentations**: Scripts in ``resources/client_gen/augmentations/`` modify OpenAPI specs before generation (e.g., add missing authentication schemes)
- **Configuration**: Client generation controlled by ``resources/client_gen/generate_api_client.sh``

The generated clients replace the existing ``nipyapi/nifi/`` and ``nipyapi/registry/`` packages. Always test thoroughly after regeneration and commit the changes as a cohesive unit.



Release Process
---------------

Streamlined release workflow using our modern build system. Assumes development environment is set up (``make dev-install`` completed).

Pre-release Preparation
~~~~~~~~~~~~~~~~~~~~~~~

1. **Update Release Notes**:

   Update ``docs/history.rst`` with comprehensive release notes including new features, breaking changes, bug fixes, and migration guidance.

2. **Validate Project State**:

   .. code-block:: shell

       # Ensure clean working directory
       git status

       # Full rebuild: clean -> certs -> specs -> client generation -> tests -> build -> validate -> docs
       make rebuild-all

3. **Commit Release Preparation**:

   .. code-block:: shell

       git add docs/history.rst
       git commit -S -m "Prepare release: update history and documentation"

Build and Quality Assurance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # Build fresh distributions for release (rebuild-all already validated them)
    make clean-all
    make dist

Create Release
~~~~~~~~~~~~~~

.. code-block:: shell

    # Tag the release (triggers version detection via setuptools-scm)
    git tag -a -s v1.0.0 -m "Release 1.0.0"

    # Push commit and tags to GitHub (triggers CI validation)
    git push origin main
    git push --tags

Publish to PyPI
~~~~~~~~~~~~~~~

.. code-block:: shell

    # Upload to PyPI (requires PyPI API token configured)
    twine upload dist/*

    # Alternative: Upload to TestPyPI first for validation
    # twine upload --repository testpypi dist/*

Post-release Verification
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **GitHub**: Verify release appears in GitHub Releases page
2. **PyPI**: Check package page, metadata, and download links
3. **Documentation**: Confirm ReadTheDocs rebuild triggered and succeeded
4. **Installation Test**:

   .. code-block:: shell

       # Test installation in clean environment
       pip install nipyapi=={version}
       python -c "import nipyapi; print(nipyapi.__version__)"

Version Management Notes
~~~~~~~~~~~~~~~~~~~~~~~~

- **Automatic Versioning**: ``setuptools-scm`` generates versions from git tags and commits
- **Development Versions**: Commits after tags get ``.devN+gHASH`` suffix automatically
- **Release Versions**: Clean git tags (e.g., ``v1.0.0``) produce clean versions (``1.0.0``)
- **Pre-releases**: Use tag patterns like ``v1.0.0rc1`` for release candidates
