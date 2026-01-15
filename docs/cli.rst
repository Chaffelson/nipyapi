.. highlight:: shell

======================
Command-Line Interface
======================

NiPyAPI provides a command-line interface (CLI) for automating Apache NiFi operations. The CLI exposes all nipyapi modules and functions, making it suitable for shell scripting, CI/CD pipelines, and interactive exploration.

Installation
============

**With pip (standard installation):**

.. code-block:: console

    pip install "nipyapi[cli]"

**With uv (faster installation):**

.. code-block:: console

    uv pip install "nipyapi[cli]"

**Without installation (ephemeral):**

.. code-block:: console

    uvx --from "nipyapi[cli]" nipyapi system get_nifi_version_info

**From source (development):**

.. code-block:: console

    pip install "nipyapi[cli] @ git+https://github.com/Chaffelson/nipyapi.git@feature/cli"

Configuration
=============

The CLI auto-detects configuration using this priority:

1. ``--profile`` argument (explicit profile selection)
2. Environment variables (if ``NIFI_API_ENDPOINT`` is set)
3. ``NIPYAPI_PROFILE`` env var (selects named profile from profiles file)
4. First profile in ``~/.nipyapi/profiles.yml``
5. No configuration (commands will fail with helpful error)

Environment Variables
---------------------

For CI/CD environments, configure using environment variables:

.. code-block:: console

    # Required - NiFi connection
    export NIFI_API_ENDPOINT="https://nifi.example.com/nifi-api"

    # Authentication (choose one method)
    export NIFI_BEARER_TOKEN="eyJhbGciOiJSUzI1NiI..."  # JWT token
    # OR
    export NIFI_USERNAME="admin"
    export NIFI_PASSWORD="password"

    # Optional - SSL/TLS
    export NIFI_VERIFY_SSL="true"  # Set to "false" for self-signed certs

User Profiles File
------------------

For interactive use, create ``~/.nipyapi/profiles.yml``:

.. code-block:: yaml

    production:
      nifi_url: "https://nifi.production.example.com/nifi-api"
      nifi_bearer_token: "eyJhbGciOiJSUzI1NiI..."
      nifi_verify_ssl: true

    development:
      nifi_url: "https://localhost:9443/nifi-api"
      nifi_user: "admin"
      nifi_pass: "password"
      nifi_verify_ssl: false

See :doc:`profiles` for complete configuration options.

Profile Selection
=================

Use the ``--profile`` option to explicitly select a profile:

.. code-block:: console

    # Explicit profile selection (recommended for multi-profile setups)
    nipyapi --profile production system get_nifi_version_info
    nipyapi --profile development ci get_status

    # The --profile option must come before the subcommand
    nipyapi --profile <profile_name> <module> <command> [args]

Discovering Commands
====================

The CLI is built on Google Fire, which provides built-in help and introspection:

.. code-block:: console

    # List all available modules
    nipyapi --help

    # List all functions in a module
    nipyapi canvas --help
    nipyapi versioning --help

    # Get help for a specific function (shows parameters and docstring)
    nipyapi canvas get_process_group --help
    nipyapi ci deploy_flow --help

    # Show function signature
    nipyapi versioning list_registry_clients -- --help

Use ``--help`` at any level to explore available commands and their parameters.

Available Modules
=================

The CLI exposes nipyapi's high-level helper modules, which provide user-friendly
abstractions over the NiFi and Registry APIs. Use ``nipyapi <module> --help`` to
see the complete list of functions for any module.

**Note:** The low-level ``nipyapi.nifi`` and ``nipyapi.registry`` API clients are not
exposed via CLI as they require complex object inputs better suited for Python usage.
See :doc:`nipyapi-docs/api_reference` for the complete API including low-level clients.

For full API documentation including all parameters, types, and detailed descriptions,
see :doc:`nipyapi-docs/api_reference`.

**ci** - CI/CD Operations
    High-level operations for flow deployment and management in CI/CD pipelines.
    See :doc:`ci` for complete documentation of all CI functions.

    .. code-block:: console

        nipyapi ci --help                    # List all CI operations
        nipyapi ci deploy_flow --help        # Help for specific operation

**canvas** - Process Groups and Processors
    Core NiFi canvas operations: process groups, processors, connections, ports.

    .. code-block:: console

        nipyapi canvas --help                # List all canvas functions
        nipyapi canvas get_root_pg_id
        nipyapi canvas list_all_process_groups
        nipyapi canvas get_process_group PG_ID id

    See :doc:`nipyapi-docs/core_modules/canvas` for full API reference.

**versioning** - Flow Registry
    Flow versioning, registry clients, and version control operations.

    .. code-block:: console

        nipyapi versioning --help            # List all versioning functions
        nipyapi versioning list_registry_clients
        nipyapi versioning get_version_info PROCESS_GROUP

    See :doc:`nipyapi-docs/core_modules/versioning` for full API reference.

**parameters** - Parameter Contexts
    Parameter context management, inheritance, and assets.

    .. code-block:: console

        nipyapi parameters --help            # List all parameter functions
        nipyapi parameters list_all_parameter_contexts
        nipyapi parameters get_parameter_context CONTEXT_ID id

    See :doc:`nipyapi-docs/core_modules/parameters` for full API reference.

**security** - Users and Policies
    User, group, and access policy management.

    .. code-block:: console

        nipyapi security --help              # List all security functions
        nipyapi security list_service_users

    See :doc:`nipyapi-docs/core_modules/security` for full API reference.

**system** - Cluster Information
    System diagnostics, cluster status, and NiFi information.

    .. code-block:: console

        nipyapi system --help                # List all system functions
        nipyapi system get_nifi_version_info

    See :doc:`nipyapi-docs/core_modules/system` for full API reference.

**layout** - Canvas Layout
    Utilities for arranging and organizing components on the canvas.

    .. code-block:: console

        nipyapi layout --help                # List all layout functions
        nipyapi layout align_pg_grid PG_ID --sort_by_name=True

**config** - Configuration
    Access to nipyapi configuration settings.

    .. code-block:: console

        nipyapi config --help                # List config attributes

    See :doc:`nipyapi-docs/core_modules/config` for full API reference.

**profiles** - Profile Management
    Profile loading and switching functions.

    .. code-block:: console

        nipyapi profiles --help              # List profile functions

    See :doc:`nipyapi-docs/core_modules/profiles` for full API reference.

**utils** - Utilities
    Helper functions for common operations.

    .. code-block:: console

        nipyapi utils --help                 # List utility functions

    See :doc:`nipyapi-docs/core_modules/utils` for full API reference.

Output Formatting
=================

The CLI automatically formats output based on the execution environment:

**JSON (default)**
    Structured JSON output for programmatic parsing.

    .. code-block:: console

        nipyapi system get_nifi_version_info
        # Output: {"niFi_version": "2.0.0", ...}

**GitHub Actions**
    Auto-detected when ``GITHUB_ACTIONS`` env var is set. Outputs ``key=value`` pairs
    compatible with ``$GITHUB_OUTPUT``. Keys are converted from snake_case to kebab-case.

    .. code-block:: console

        # In GitHub Actions workflow
        nipyapi ci deploy_flow ... >> $GITHUB_OUTPUT
        # Output: process-group-id=abc-123

**GitLab CI (dotenv)**
    Auto-detected when ``GITLAB_CI`` env var is set. Outputs ``KEY=VALUE`` pairs
    for dotenv artifact format. Keys are converted to UPPER_SNAKE_CASE.

    .. code-block:: console

        # In GitLab CI job
        nipyapi ci deploy_flow ... > deploy.env
        # Output: PROCESS_GROUP_ID=abc-123

**Manual Override**
    Force a specific format using ``NIFI_OUTPUT_FORMAT``:

    .. code-block:: console

        export NIFI_OUTPUT_FORMAT=json    # JSON (default)
        export NIFI_OUTPUT_FORMAT=github  # GitHub Actions format
        export NIFI_OUTPUT_FORMAT=dotenv  # GitLab dotenv format

Log Level Control
=================

Control log verbosity using ``NIFI_LOG_LEVEL``:

.. code-block:: console

    export NIFI_LOG_LEVEL=WARNING  # Default - only warnings and errors
    export NIFI_LOG_LEVEL=ERROR    # Only errors
    export NIFI_LOG_LEVEL=INFO     # Normal operational info
    export NIFI_LOG_LEVEL=DEBUG    # Full debug output

On error, logs are included in the output by default. Disable with:

.. code-block:: console

    export NIFI_LOG_ON_ERROR=false

Usage Examples
==============

**Test connectivity:**

.. code-block:: console

    nipyapi system get_nifi_version_info

**List all process groups:**

.. code-block:: console

    nipyapi canvas list_all_process_groups

**Get process group by ID:**

.. code-block:: console

    nipyapi canvas get_process_group "abc-123-def" id

**Get registry client by name:**

.. code-block:: console

    nipyapi versioning get_registry_client "MyRegistryClient"

**Deploy a flow from registry:**

.. code-block:: console

    nipyapi ci deploy_flow \
        --registry_client_id "$REGISTRY_ID" \
        --bucket "connectors" \
        --flow "postgresql"

**Parse JSON output with jq:**

.. code-block:: console

    # Get registry client ID by name
    REGISTRY_ID=$(nipyapi versioning get_registry_client "MyClient" | jq -r '.id')

    # List process group names
    nipyapi canvas list_all_process_groups | jq -r '.[].component.name'

Error Handling
==============

The CLI returns structured error responses and uses non-zero exit codes for failures.

**Exception errors** (Python exceptions during execution):

.. code-block:: json

    {
      "success": false,
      "error": "Process group not found: invalid-id",
      "error_type": "ValueError",
      "command": "get_process_group",
      "logs": ["nipyapi.canvas: Fetching process group..."]
    }

**Operational errors** (command completed but operation failed):

CI functions include an ``error`` or ``errors`` field when an operation fails.
The CLI detects these fields and exits with code 1.

.. code-block:: json

    {
      "verified": "false",
      "failed_count": 2,
      "error": "Verification failed for: DBCPConnectionPool, ExecuteSQL"
    }

Exit codes:

- ``0``: Success (no ``error``/``errors`` key in result)
- ``1``: Error (exception raised, or result contains ``error``/``errors`` key)

Error Field Convention
----------------------

When writing custom CI functions or extending nipyapi, follow this convention:

- Include an ``error`` key (string) when an operation fails
- Use ``errors`` key (string) for multiple error messages (pipe-separated)
- Do NOT include ``error``/``errors`` keys on success

This ensures the CLI exits with the correct code for scripting:

.. code-block:: bash

    # Script can rely on exit code
    if nipyapi ci verify_config --process_group_id "$PG_ID"; then
        nipyapi ci start_flow --process_group_id "$PG_ID"
    else
        echo "Verification failed, not starting flow"
        exit 1
    fi

Cross-References
================

**For CI/CD operations:** See :doc:`ci`

**For profile configuration:** See :doc:`profiles`

**For security setup:** See :doc:`security`

**For API reference:** See :doc:`nipyapi-docs/api_reference`
