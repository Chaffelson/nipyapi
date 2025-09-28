Dependencies
-------------

NiPyAPI automatically manages its dependencies during installation. Here are the complete dependency details, automatically generated from the actual project dependency files.

Runtime Dependencies
--------------------

These dependencies are automatically installed when you install NiPyAPI:


**Core HTTP Stack:**

- ``certifi>=2023.7.22`` - SSL certificate verification
- ``pysocks>=1.7.1`` - SOCKS proxy support
- ``requests>=2.18`` - Primary HTTP client for API communication
- ``urllib3>=1.26,<3`` - HTTP client backend and connection pooling

**Utilities:**

- ``PyYAML>=6.0`` - YAML file processing and serialization
- ``packaging>=17.1`` - Version comparison utilities

**Build & Packaging:**

- ``setuptools>=38.5`` - Package management and distribution

Optional Dependencies
---------------------

**Development Dependencies** (install with ``pip install nipyapi[dev]``):

- ``codecov>=2.1.13`` - Coverage reporting service integration
- ``coverage>=7.0`` - Coverage analysis and reporting
- ``deepdiff>=3.3.0`` - Deep data structure comparison for testing
- ``flake8>=3.6.0`` - Code style and syntax checking
- ``pre-commit>=3.0.0`` - Development tool
- ``pylint>=3.3.0`` - Advanced code analysis and linting
- ``pytest-cov>=5.0.0`` - Test coverage measurement
- ``pytest>=8.4`` - Testing framework
- ``twine>=6.0.0`` - Package distribution to PyPI

**Documentation Dependencies** (install with ``pip install nipyapi[docs]``):

- ``Sphinx>=7.4.0`` - Documentation generation framework
- ``sphinx_rtd_theme>=3.0.0`` - Read the Docs theme for Sphinx
- ``sphinxcontrib-jquery>=4.1`` - jQuery support for Sphinx themes

Dependency Management
---------------------

**Automatic Installation:**
All runtime dependencies are automatically installed when you install NiPyAPI via pip.

**Version Constraints:**
NiPyAPI specifies minimum versions for compatibility but allows newer versions unless there are known incompatibilities.

**Development Setup:**
For a complete development environment with all optional dependencies:

.. code-block:: console

    $ pip install -e ".[dev,docs]"

**Minimal Installation:**
NiPyAPI requires only 7 runtime dependencies for basic functionality.

.. note::
   This dependency information is automatically generated from the project's
   ``requirements.txt`` and ``pyproject.toml`` files during documentation build.

