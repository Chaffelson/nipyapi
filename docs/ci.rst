.. highlight:: shell

=============
CI Operations
=============

The ``nipyapi.ci`` module provides high-level operations designed for CI/CD pipelines. These functions wrap nipyapi operations with environment variable support, sensible defaults, and simplified interfaces.

Overview
========

CI operations are designed for automation scenarios:

- **Environment variable support**: All parameters can be set via environment variables
- **Sensible defaults**: Minimal configuration required for common use cases
- **Structured output**: Returns plain dicts suitable for CI artifact formats
- **Error handling**: Raises exceptions with clear error messages

Quick Start
===========

.. code-block:: console

    # 1. Configure NiFi connection
    export NIFI_API_ENDPOINT="https://nifi.example.com/nifi-api"
    export NIFI_BEARER_TOKEN="your-jwt-token"

    # 2. Set up registry client
    export GH_REGISTRY_TOKEN="ghp_xxxx"
    nipyapi ci ensure_registry --repo owner/repo

    # 3. Deploy a flow
    nipyapi ci deploy_flow --bucket connectors --flow postgresql

    # 4. Start the flow
    nipyapi ci start_flow --process_group_id $PROCESS_GROUP_ID

Available Operations
====================

ensure_registry
---------------

Create or update a Git Flow Registry Client (GitHub or GitLab).

.. code-block:: console

    nipyapi ci ensure_registry \
        --token TOKEN \
        --repo owner/repo \
        --client_name "MyRegistryClient" \
        --provider github \
        --default_branch main

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--token``                    Personal Access Token                         ``GH_REGISTRY_TOKEN`` or ``GL_REGISTRY_TOKEN``
``--repo``                     Repository in owner/repo format               ``NIFI_REGISTRY_REPO``
``--client_name``              Registry client name                          ``NIFI_REGISTRY_CLIENT_NAME``
``--provider``                 Git provider (github/gitlab)                  ``NIFI_REGISTRY_PROVIDER``
``--api_url``                  API URL override                              ``NIFI_REGISTRY_API_URL``
``--default_branch``           Default branch (default: main)                ``NIFI_REGISTRY_BRANCH``
``--repository_path``          Path within repository                        ``NIFI_REPOSITORY_PATH``
=============================  ============================================  ================================

**Returns:** ``registry_client_id``, ``registry_client_name``

deploy_flow
-----------

Deploy a flow from a Git-based registry to the NiFi canvas.

.. code-block:: console

    nipyapi ci deploy_flow \
        --registry_client_id REGISTRY_ID \
        --bucket connectors \
        --flow postgresql \
        --branch main \
        --version v1.0.0

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--registry_client_id``       ID of the registry client                     ``NIFI_REGISTRY_CLIENT_ID``
``--bucket``                   Bucket (folder) containing the flow           ``NIFI_BUCKET``
``--flow``                     Flow name (filename without .json)            ``NIFI_FLOW``
``--parent_id``                Parent Process Group ID (default: root)       ``NIFI_PARENT_ID``
``--branch``                   Branch to deploy from                         ``NIFI_FLOW_BRANCH``
``--version``                  Version (commit SHA, tag, branch)             ``NIFI_TARGET_VERSION``
``--location``                 (x, y) tuple for canvas placement             ``NIFI_LOCATION_X``, ``NIFI_LOCATION_Y``
=============================  ============================================  ================================

**Returns:** ``process_group_id``, ``process_group_name``, ``deployed_version``

start_flow
----------

Start a process group (enable controllers, start processors).

.. code-block:: console

    nipyapi ci start_flow --process_group_id PG_ID

**Parameters:**

=============================  ==================================================  ================================
Parameter                      Description                                         Environment Variable
=============================  ==================================================  ================================
``--process_group_id``         ID of the process group                             ``NIFI_PROCESS_GROUP_ID``
``--enable_controllers``       Enable controller services first (default: True)    (none)
=============================  ==================================================  ================================

**Returns:** ``started``, ``process_group_name``

stop_flow
---------

Stop a process group (stop processors, optionally disable controllers).

.. code-block:: console

    nipyapi ci stop_flow --process_group_id PG_ID
    nipyapi ci stop_flow --process_group_id PG_ID --disable_controllers

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         ID of the process group                       ``NIFI_PROCESS_GROUP_ID``
``--disable_controllers``      Also disable controller services              ``NIFI_DISABLE_CONTROLLERS``
=============================  ============================================  ================================

**Returns:** ``stopped``, ``process_group_name``, ``controllers_disabled``

get_status
----------

Get comprehensive status information for a process group.

.. code-block:: console

    nipyapi ci get_status --process_group_id PG_ID
    nipyapi ci get_status  # Uses root process group

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         ID of the process group (default: root)       ``NIFI_PROCESS_GROUP_ID``
=============================  ============================================  ================================

**Returns:** Comprehensive status including:

- ``process_group_id``, ``process_group_name``, ``state``, ``is_root``
- Processor counts: ``total_processors``, ``running_processors``, ``stopped_processors``, ``invalid_processors``, ``disabled_processors``
- Controller counts: ``total_controllers``, ``enabled_controllers``, ``disabled_controllers``
- Queue stats: ``queued_flowfiles``, ``queued_bytes``, ``active_threads``
- Version control: ``versioned``, ``version_id``, ``flow_id``, ``version_state``, ``modified``
- Parameter context: ``has_parameter_context``, ``parameter_context_id``, ``parameter_count``
- Bulletins: ``bulletin_warnings``, ``bulletin_errors``, ``bulletin_messages``

configure_params
----------------

Configure parameters on a process group's parameter context.

.. code-block:: console

    nipyapi ci configure_params \
        --process_group_id PG_ID \
        --parameters '{"db_host": "localhost", "db_port": "5432"}'

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         ID of the process group                       ``NIFI_PROCESS_GROUP_ID``
``--parameters``               JSON string of parameter name-value pairs     ``NIFI_PARAMETERS``
=============================  ============================================  ================================

**Returns:** ``parameters_updated``, ``parameters_count``, ``context_name``

**Note:** This function only updates parameters in the directly attached parameter context.
If your flow uses parameter context inheritance, use ``configure_inherited_params`` instead.

configure_inherited_params
--------------------------

Configure parameters across an inheritance hierarchy, routing each parameter to its owning context.

This function is **inheritance-aware**: it determines which parameter context owns each parameter
and updates it in the correct context, preventing accidental shadowing. It also supports dry-run
mode to preview changes before applying them.

.. code-block:: console

    # Dry run first (always recommended)
    nipyapi ci configure_inherited_params \
        --process_group_id PG_ID \
        --parameters '{"Source Username": "myuser", "Snowflake Warehouse": "my_wh"}' \
        --dry_run

    # Execute after confirming the plan
    nipyapi ci configure_inherited_params \
        --process_group_id PG_ID \
        --parameters '{"Source Username": "myuser", "Snowflake Warehouse": "my_wh"}'

**Parameters:**

=============================  ====================================================  ================================
Parameter                      Description                                           Environment Variable
=============================  ====================================================  ================================
``--process_group_id``         ID of the process group                               ``NIFI_PROCESS_GROUP_ID``
``--parameters``               JSON string of parameter name-value pairs             ``NIFI_PARAMETERS``
``--dry_run``                  Preview changes without applying (default: false)     ``NIFI_DRY_RUN``
``--allow_override``           Create parameters at top level if not found           ``NIFI_ALLOW_OVERRIDE``
=============================  ====================================================  ================================

**Returns:**

- ``dry_run``: Whether this was a dry run
- ``plan``: Summary of planned/executed updates (e.g., ``Param1→Context1 | Param2→Context2``)
- ``parameters_updated``: Count of parameters updated (0 if dry run)
- ``contexts_modified``: Count of contexts modified (0 if dry run)
- ``warnings``: Any warnings (e.g., asset replacement)
- ``errors``: Any errors (e.g., parameter not found)

**When to use this vs configure_params:**

- Use ``configure_params`` for simple flows with a single parameter context
- Use ``configure_inherited_params`` when your flow has inherited parameter contexts (common with
  connectors that separate source, destination, and flow-specific parameters)

change_version
--------------

Change the version of a deployed flow.

.. code-block:: console

    nipyapi ci change_version --process_group_id PG_ID --target_version v2.0.0
    nipyapi ci change_version --process_group_id PG_ID  # Changes to latest

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         ID of the process group                       ``NIFI_PROCESS_GROUP_ID``
``--target_version``           Version (commit SHA, tag, branch)             ``NIFI_TARGET_VERSION``
``--branch``                   Branch to use                                 ``NIFI_FLOW_BRANCH``
``--token``                    Git token for resolving tags                  ``GH_REGISTRY_TOKEN`` or ``GL_REGISTRY_TOKEN``
``--repo``                     Repository in owner/repo format               ``NIFI_REGISTRY_REPO``
``--provider``                 Git provider (github/gitlab)                  ``NIFI_REGISTRY_PROVIDER``
=============================  ============================================  ================================

**Returns:** ``previous_version``, ``new_version``, ``version_state``

revert_flow
-----------

Revert uncommitted local changes to a flow.

.. code-block:: console

    nipyapi ci revert_flow --process_group_id PG_ID

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         ID of the process group                       ``NIFI_PROCESS_GROUP_ID``
=============================  ============================================  ================================

**Returns:** ``reverted``, ``process_group_name``, ``version``

cleanup
-------

Stop and optionally delete a process group.

.. code-block:: console

    # Just stop (safest)
    nipyapi ci cleanup --process_group_id PG_ID --stop_only

    # Stop and delete process group
    nipyapi ci cleanup --process_group_id PG_ID

    # Full cleanup including parameter context
    nipyapi ci cleanup --process_group_id PG_ID --delete_parameter_context --force

**Parameters:**

================================  ==========================================  ====================================
Parameter                         Description                                 Environment Variable
================================  ==========================================  ====================================
``--process_group_id``            ID of the process group                     ``NIFI_PROCESS_GROUP_ID``
``--stop_only``                   Only stop, don't delete                     ``NIFI_STOP_ONLY``
``--force``                       Force deletion with queued FlowFiles        ``NIFI_FORCE_DELETE``
``--delete_parameter_context``    Also delete the parameter context           ``NIFI_DELETE_PARAMETER_CONTEXT``
``--disable_controllers``         Disable controllers (default: true)         ``NIFI_DISABLE_CONTROLLERS``
================================  ==========================================  ====================================

**Returns:** ``stopped``, ``deleted``, ``process_group_name``, ``parameter_context_deleted``

get_versions
------------

List version control state for all process groups under a parent.

This function scans process groups and reports their version control status, making it
easy to identify which flows need updates, have local modifications, or are out of sync.

.. code-block:: console

    # List immediate child process groups from root
    nipyapi ci get_versions

    # List all process groups recursively
    nipyapi ci get_versions --descendants

    # List process groups under a specific parent
    nipyapi ci get_versions --process_group_id PG_ID

**Parameters:**

=============================  ============================================  ================================
Parameter                      Description                                   Environment Variable
=============================  ============================================  ================================
``--process_group_id``         Parent PG to search from (default: root)      ``NIFI_PROCESS_GROUP_ID``
``--descendants``              Include all nested PGs recursively            ``NIFI_INCLUDE_DESCENDANTS``
=============================  ============================================  ================================

**Returns:**

- ``parent_id``, ``parent_name``: The parent process group searched from
- ``total_count``: Total number of process groups found
- ``versioned_count``: Number of version-controlled process groups
- ``stale_count``: Number with available updates
- ``modified_count``: Number with local modifications
- ``process_groups``: List of dicts with version info for each PG:
  - ``id``, ``name``: Process group identification
  - ``versioned``: Whether under version control
  - ``current_version``: Current version (or empty)
  - ``state``: Version state (UP_TO_DATE, STALE, LOCALLY_MODIFIED, etc.)
  - ``modified``: Whether local changes exist
  - ``flow_name``, ``bucket_name``: Registry flow info

purge_flowfiles
---------------

Purge queued FlowFiles from a process group.

.. code-block:: console

    nipyapi ci purge_flowfiles --process_group_id PG_ID

**Returns:** ``purged``, ``process_group_name``

upload_asset
------------

Upload an asset file to a process group.

.. code-block:: console

    nipyapi ci upload_asset --process_group_id PG_ID --file_path /path/to/asset.jar

**Returns:** ``uploaded``, ``asset_id``, ``asset_name``

resolve_git_ref
---------------

Resolve a git reference (tag, branch, or partial SHA) to a full commit SHA.

This utility function is used internally by ``change_version`` and ``deploy_flow``, but can
also be called directly when you need to resolve a git ref before passing it to other operations.

.. code-block:: console

    # Resolve a tag to SHA
    nipyapi ci resolve_git_ref --ref v1.0.0 --repo owner/repo --token $GH_TOKEN

    # Resolve a branch to SHA
    nipyapi ci resolve_git_ref --ref main --repo owner/repo --token $GH_TOKEN --provider github

    # Already a SHA - returns as-is (no API call needed)
    nipyapi ci resolve_git_ref --ref abc123def456

**Parameters:**

==================  ================================================  ========================================
Parameter           Description                                       Environment Variable
==================  ================================================  ========================================
``--ref``           Tag name, branch name, or commit SHA              (none)
``--repo``          Repository in owner/repo format                   ``NIFI_REGISTRY_REPO``
``--token``         Personal access token for API access              ``GH_REGISTRY_TOKEN`` / ``GL_REGISTRY_TOKEN``
``--provider``      Git provider: github/gitlab (default: github)     ``NIFI_REGISTRY_PROVIDER``
==================  ================================================  ========================================

**Returns:** The resolved commit SHA, or None if ref was empty.

**Notes:**

- If the ref already looks like a SHA (7-40 hex characters), it's returned as-is without an API call
- Useful for CI/CD pipelines that need to pin to exact commits
- Called automatically by ``change_version`` when you pass a tag or branch name

Environment Variable Reference
==============================

Connection
----------

=============================  ============================================
Variable                       Description
=============================  ============================================
``NIFI_API_ENDPOINT``          NiFi API URL
``NIFI_BEARER_TOKEN``          JWT bearer token
``NIFI_USERNAME``              Basic auth username
``NIFI_PASSWORD``              Basic auth password
``NIFI_VERIFY_SSL``            SSL verification (default: true)
=============================  ============================================

Registry
--------

=============================  ============================================
Variable                       Description
=============================  ============================================
``GH_REGISTRY_TOKEN``          GitHub Personal Access Token
``GL_REGISTRY_TOKEN``          GitLab Personal Access Token
``NIFI_REGISTRY_REPO``         Repository in owner/repo format
``NIFI_REGISTRY_CLIENT_ID``    Registry client ID
``NIFI_REGISTRY_CLIENT_NAME``  Registry client name
``NIFI_REGISTRY_PROVIDER``     Git provider (github/gitlab)
``NIFI_REGISTRY_API_URL``      API URL override
``NIFI_REGISTRY_BRANCH``       Default branch
``NIFI_REPOSITORY_PATH``       Path within repository
=============================  ============================================

Flow Operations
---------------

=============================  ============================================
Variable                       Description
=============================  ============================================
``NIFI_PROCESS_GROUP_ID``      Process group ID
``NIFI_PARENT_ID``             Parent process group ID
``NIFI_BUCKET``                Bucket (folder) name
``NIFI_FLOW``                  Flow name
``NIFI_FLOW_BRANCH``           Branch for deployment
``NIFI_TARGET_VERSION``        Target version (SHA, tag, branch)
``NIFI_LOCATION_X``            Canvas X coordinate
``NIFI_LOCATION_Y``            Canvas Y coordinate
``NIFI_PARAMETERS``            JSON parameter values
=============================  ============================================

Cleanup
-------

===================================  ============================================
Variable                             Description
===================================  ============================================
``NIFI_STOP_ONLY``                   Only stop, don't delete (true/false)
``NIFI_FORCE_DELETE``                Force deletion (true/false)
``NIFI_DELETE_PARAMETER_CONTEXT``    Delete parameter context (true/false)
``NIFI_DISABLE_CONTROLLERS``         Disable controllers (true/false)
===================================  ============================================

Complete Workflow Example
=========================

Shell Script
------------

.. code-block:: bash

    #!/bin/bash
    set -e

    # Configuration
    export NIFI_API_ENDPOINT="https://nifi.example.com/nifi-api"
    export NIFI_BEARER_TOKEN="$NIFI_TOKEN"
    export GH_REGISTRY_TOKEN="$GITHUB_TOKEN"

    # 1. Ensure registry client exists
    RESULT=$(nipyapi ci ensure_registry --repo myorg/nifi-flows)
    REGISTRY_ID=$(echo "$RESULT" | jq -r '.registry_client_id')
    echo "Registry client: $REGISTRY_ID"

    # 2. Deploy the flow
    RESULT=$(nipyapi ci deploy_flow \
        --registry_client_id "$REGISTRY_ID" \
        --bucket connectors \
        --flow postgresql \
        --version "$FLOW_VERSION")
    PG_ID=$(echo "$RESULT" | jq -r '.process_group_id')
    echo "Deployed process group: $PG_ID"

    # 3. Configure parameters
    nipyapi ci configure_params \
        --process_group_id "$PG_ID" \
        --parameters '{"db_host": "'"$DB_HOST"'", "db_password": "'"$DB_PASSWORD"'"}'

    # 4. Start the flow
    nipyapi ci start_flow --process_group_id "$PG_ID"

    # 5. Verify status
    nipyapi ci get_status --process_group_id "$PG_ID"

GitHub Actions
--------------

For GitHub Actions integration, use the `nipyapi-actions <https://github.com/Chaffelson/nipyapi-actions>`_ repository which provides reusable actions:

.. code-block:: yaml

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - name: Deploy NiFi Flow
            uses: Chaffelson/nipyapi-actions@main
            with:
              operation: deploy-flow
              nifi-api-endpoint: ${{ secrets.NIFI_API_ENDPOINT }}
              nifi-token: ${{ secrets.NIFI_TOKEN }}
              registry-token: ${{ secrets.GH_REGISTRY_TOKEN }}
              registry-repo: ${{ github.repository }}
              bucket: connectors
              flow: postgresql

GitLab CI
---------

For GitLab CI, include the fragments template:

.. code-block:: yaml

    include:
      - remote: 'https://raw.githubusercontent.com/Chaffelson/nipyapi-actions/main/templates/fragments.yml'

    variables:
      NIFI_API_ENDPOINT: "https://nifi.example.com/nifi-api"
      NIFI_REGISTRY_REPO: "mygroup/nifi-flows"
      NIFI_BUCKET: "connectors"
      NIFI_FLOW: "postgresql"

    deploy:
      image: python:3.11
      before_script:
        - !reference [.nipyapi, setup]
      script:
        - !reference [.nipyapi, ensure-registry]
        - !reference [.nipyapi, deploy-flow]
        - !reference [.nipyapi, start-flow]

Python Usage
============

CI functions can also be used directly in Python:

.. code-block:: python

    import os
    import nipyapi

    # Configure connection
    nipyapi.profiles.switch('production')

    # Or use environment variables
    os.environ['GH_REGISTRY_TOKEN'] = 'ghp_xxxx'

    # Ensure registry client
    result = nipyapi.ci.ensure_registry(
        repo='myorg/nifi-flows',
        client_name='MyRegistryClient'
    )
    registry_id = result['registry_client_id']

    # Deploy flow
    result = nipyapi.ci.deploy_flow(
        registry_client_id=registry_id,
        bucket='connectors',
        flow='postgresql'
    )
    pg_id = result['process_group_id']

    # Start flow
    nipyapi.ci.start_flow(process_group_id=pg_id)

    # Get status
    status = nipyapi.ci.get_status(process_group_id=pg_id)
    print(f"State: {status['state']}, Running: {status['running_processors']}")

Cross-References
================

**For CLI usage:** See :doc:`cli`

**For profile configuration:** See :doc:`profiles`

**For version control details:** See :doc:`nipyapi-docs/core_modules/versioning`

**For GitHub Actions:** See `nipyapi-actions <https://github.com/Chaffelson/nipyapi-actions>`_
