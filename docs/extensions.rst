.. highlight:: python

================================
Working with NiFi Extensions
================================

NiPyAPI provides tooling for managing NiFi extensions (NAR files) and their associated
components, including Python-based processors that require special handling during initialization.

This guide covers operational aspects of working with extensions that supplement the official
`NiFi Python Developer's Guide <https://nifi.apache.org/documentation/>`_ which focuses on authoring.

.. note::
   **Development vs Operations:**

   - **NiFi Python Developer's Guide**: How to write Python processors
   - **This Document**: How to deploy, monitor, and manage extensions in production

Key Concepts
============

**NAR (NiFi Archive)**
    A bundle containing processors, controller services, or other NiFi components.
    NARs are the standard packaging format for NiFi extensions.

**Extension**
    A custom component type (processor, controller service, etc.) provided by a NAR.

**Python Processor**
    A processor written in Python that requires virtual environment setup before use.
    These processors have unique initialization characteristics.

**NAR Coordinate**
    The unique identifier for a NAR consisting of ``group:artifact:version`` (GAV).
    For example: ``my-company:my-processors-nar:1.0.0``.

Extension Management
====================

Listing Installed Extensions
----------------------------

View all NARs installed in the NiFi instance:

.. code-block:: python

    import nipyapi

    # List all NARs
    nars = nipyapi.extensions.list_nars()
    for nar in nars:
        print(f"{nar.coordinate} - {nar.state}")

Or via CLI:

.. code-block:: shell

    nipyapi ci list_nars

Uploading Extensions
--------------------

Upload a NAR file to NiFi. The upload waits for installation to complete:

.. code-block:: python

    import nipyapi

    # Upload and wait for installation
    nar = nipyapi.extensions.upload_nar("/path/to/my-processor.nar")
    print(f"Installed: {nar.identifier}")
    print(f"Coordinate: {nar.coordinate}")
    print(f"State: {nar.state}")

Or via CLI:

.. code-block:: shell

    nipyapi ci upload_nar --nar_file /path/to/my-processor.nar

The function returns only after the NAR is fully installed and ready to deploy components from.

Getting NAR Details
-------------------

Retrieve detailed information about an installed NAR, including its component types:

.. code-block:: python

    import nipyapi

    # Get NAR with full details
    details = nipyapi.extensions.get_nar_details(nar_id)

    print("Processor types:")
    for proc_type in details.processor_types:
        print(f"  - {proc_type.type}")

    print("Controller service types:")
    for cs_type in details.controller_service_types:
        print(f"  - {cs_type.type}")

Finding a NAR by Coordinate
---------------------------

Look up a NAR using its Maven coordinates:

.. code-block:: python

    import nipyapi

    nar = nipyapi.extensions.get_nar_by_coordinate(
        group_id="my-company",
        artifact_id="my-processors-nar",
        version="1.0.0"
    )

Downloading Extensions
----------------------

Download an installed NAR to a local file:

.. code-block:: python

    import nipyapi

    nipyapi.extensions.download_nar(nar_id, "/path/to/save/my-processor.nar")

Deleting Extensions
-------------------

Remove an installed NAR:

.. code-block:: python

    import nipyapi

    # Safe delete - fails if components are using the NAR
    nipyapi.extensions.delete_nar(nar_id)

    # Force delete - removes NAR even if components are using it
    # WARNING: This orphans any components using the NAR
    nipyapi.extensions.delete_nar(nar_id, force=True)

Or via CLI:

.. code-block:: shell

    # Safe delete
    nipyapi ci delete_nar --identifier <nar_id>

    # Force delete
    nipyapi ci delete_nar --identifier <nar_id> --force

    # Delete by coordinate
    nipyapi ci delete_nar --group_id my-company --artifact_id my-nar --version 1.0.0

Python Processor Initialization
===============================

Python processors require additional initialization time after creation as they must set up their virtual environment and
download dependencies before they can be configured.

Initialization States
---------------------

Python processors go through several states during initialization:

.. list-table:: Processor Initialization States
   :header-rows: 1
   :widths: 20 20 60

   * - State
     - Properties Loaded
     - Description
   * - ``initializing``
     - No
     - Setting up Python virtual environment
   * - ``downloading_dependencies``
     - No
     - Downloading packages from PyPI
   * - ``dependency_failed``
     - No
     - Failed to download dependencies (network issue)
   * - ``ready``
     - Yes
     - Processor initialized and ready for configuration
   * - ``missing_nar``
     - No
     - NAR has been removed, processor is orphaned
   * - ``error``
     - No
     - Unknown error state

Checking Initialization Status
------------------------------

Monitor the initialization status of a processor:

.. code-block:: python

    import nipyapi

    status = nipyapi.extensions.get_processor_init_status(processor_id)

    print(f"Status: {status['status']}")
    print(f"Ready: {status['is_ready']}")
    print(f"Has Properties: {status['has_properties']}")
    print(f"Message: {status['init_message']}")

    if status['validation_errors']:
        print("Validation Errors:")
        for error in status['validation_errors']:
            print(f"  - {error}")

Waiting for Initialization
--------------------------

Wait for a processor to complete initialization:

.. code-block:: python

    import nipyapi

    # Create processor from NAR
    proc_type = nipyapi.canvas.get_processor_type("MyPythonProcessor")
    proc = nipyapi.canvas.create_processor(
        parent_pg=parent_pg,
        processor=proc_type,
        location=(300, 300),
        name="My Processor"
    )

    # Wait for initialization (up to 60 seconds)
    try:
        initialized_proc = nipyapi.extensions.wait_for_processor_init(proc, timeout=60)
        print("Processor ready for configuration")
    except ValueError as e:
        print(f"Initialization failed: {e}")

Initialization Timeline
-----------------------

Typical initialization for a Python processor:

1. **0-5 seconds**: "Initializing runtime environment" - virtual environment setup
2. **5-30 seconds**: "Downloading third-party dependencies" - if external packages needed
3. **After download**: Properties loaded, processor ready for configuration

.. note::
   **Dependency Requirements**

   If the NiFi cluster does not have network access to download Python packages (e.g., air-gapped
   environments), Python processors with external dependencies will fail to initialize.

   In such environments, bundle all dependencies in the NAR file itself rather than relying
   on runtime downloads. See the NiFi Python Developer's Guide for NAR packaging instructions.

Virtual Environment Caching
===========================

NiFi caches Python virtual environments based on the NAR coordinate (group:artifact:version).
Understanding this caching behavior is important for deployment planning.

Caching Behavior
----------------

.. list-table:: Virtual Environment Cache Behavior
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behavior
   * - Same NAR coordinate
     - Reuses cached venv, instant initialization
   * - New version (e.g., 1.0.0 → 1.0.1)
     - Creates fresh venv, full dependency download
   * - Delete and re-upload same version
     - Clears cache, triggers fresh initialization

.. important::
   **Version bumps always trigger fresh initialization**, even if dependencies haven't changed.
   Plan for dependency download time when deploying new processor versions.

Cache Location
--------------

Virtual environments are stored in NiFi's working directory::

    $NIFI_HOME/work/python/extensions/<processor_name>/<version>/

For troubleshooting, you can delete the environment directory while NiFi is stopped to force
a fresh initialization on the next startup.

Processor Bundle Version Management
====================================

When multiple versions of the same processor type are installed (via multiple NAR files),
you can manage which bundle version an existing processor uses.

Listing Available Versions
--------------------------

Check which versions are available for a processor type:

.. code-block:: python

    import nipyapi

    versions = nipyapi.extensions.get_processor_bundle_versions("MyPythonProcessor")

    print("Available versions:")
    for v in versions:
        print(f"  - {v['bundle'].version}")

Creating Processors with Specific Versions
------------------------------------------

When multiple versions exist, use ``get_processor_type_version`` to get the correct
type for creation:

.. code-block:: python

    import nipyapi

    # Get the processor type with a specific bundle version
    proc_type = nipyapi.extensions.get_processor_type_version(
        "MyPythonProcessor",
        "0.0.2-SNAPSHOT"
    )

    # Create the processor - bundle is included automatically
    proc = nipyapi.canvas.create_processor(
        parent_pg=parent_pg,
        processor=proc_type,
        location=(300, 300),
        name="My Processor"
    )

    print(f"Created with bundle: {proc.component.bundle.version}")

Changing Processor Version
--------------------------

Change an existing processor to use a different bundle version:

.. code-block:: python

    import nipyapi

    # Get the processor
    proc = nipyapi.canvas.get_processor(processor_id, "id")
    print(f"Current version: {proc.component.bundle.version}")

    # Change to a different version
    updated = nipyapi.extensions.change_processor_bundle_version(proc, "0.0.2-SNAPSHOT")
    print(f"New version: {updated.component.bundle.version}")

.. note::
   **Before changing versions:**

   - The processor should be stopped
   - Properties and configuration are preserved
   - This changes the implementation bundle, not a version-controlled flow

Multi-Version Conflicts
-----------------------

When multiple NAR versions are installed simultaneously, creating new processors may fail:

.. code-block:: text

    409 Conflict: Multiple versions of MyProcessor exist.

**Solutions:**

1. Explicitly select the bundle version when creating processors
2. Remove older NAR versions before uploading new ones
3. Use ``change_processor_bundle_version()`` to switch existing processors

Python Processor Bundle Versioning
----------------------------------

Python processors have a unique versioning model:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description
   * - Bundle Group
     - Always ``org.apache.nifi``
   * - Bundle Artifact
     - Always ``python-extensions``
   * - Bundle Version
     - From ``ProcessorDetails.version`` in Python code

.. important::
   The bundle version for Python processors comes from the ``ProcessorDetails.version``
   attribute in your Python code, **not** from the NAR's Maven coordinate.

   Ensure you increment ``ProcessorDetails.version`` when you want distinct deployable versions
   that can coexist in the same NiFi instance.

NAR Lifecycle with Active Components
====================================

Understanding how NARs interact with deployed components is critical for production operations.

Deletion Protection
-------------------

NiFi protects NARs that have active components:

.. code-block:: python

    import nipyapi

    try:
        nipyapi.extensions.delete_nar(nar_id)
    except ValueError as e:
        # "Unable to delete NAR [...] because components are instantiated from this NAR"
        print(f"NAR protected: {e}")

Force Deletion and Orphaned Components
--------------------------------------

Force-deleting a NAR while components are using it orphans those components:

.. list-table:: NAR Deletion Effects
   :header-rows: 1
   :widths: 25 25 50

   * - Action
     - Result
     - Component State
   * - Delete NAR (no force)
     - Blocked
     - Unchanged
   * - Delete NAR (force=True)
     - NAR removed
     - STOPPED, INVALID with "Missing Processor" error
   * - Re-upload same NAR
     - NAR installed
     - Recovers to VALID, properties preserved

Recovering Orphaned Components
------------------------------

If a NAR was force-deleted and you need to recover the components:

1. Re-upload the same NAR version
2. Components automatically recover
3. Properties and configuration are preserved
4. Components can be restarted

.. code-block:: python

    import nipyapi

    # Re-upload the NAR
    nar = nipyapi.extensions.upload_nar("/path/to/my-processor.nar")

    # Wait for processor to recover
    proc = nipyapi.extensions.wait_for_processor_init(processor_id)
    print(f"Recovered: {proc.component.validation_status}")

API Reference
=============

Extensions Module Functions
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Function
     - Description
   * - ``list_nars()``
     - List all installed NARs
   * - ``get_nar(identifier)``
     - Get NAR by identifier
   * - ``get_nar_details(identifier)``
     - Get NAR with component type details
   * - ``get_nar_by_coordinate(group, artifact, version)``
     - Find NAR by Maven coordinates
   * - ``upload_nar(file_path, timeout=120)``
     - Upload NAR and wait for installation
   * - ``download_nar(identifier, file_path)``
     - Download NAR to local file
   * - ``delete_nar(identifier, force=False)``
     - Delete NAR
   * - ``get_processor_init_status(processor)``
     - Check processor initialization status
   * - ``wait_for_processor_init(processor, timeout=60)``
     - Wait for processor to initialize
   * - ``get_processor_bundle_versions(processor_type)``
     - List available bundle versions for a processor type
   * - ``get_processor_type_version(processor_type, version)``
     - Get processor type with specific bundle version for creation
   * - ``change_processor_bundle_version(processor, version)``
     - Change a processor to use a different bundle version

CI Module Functions
-------------------

Available via ``nipyapi ci`` CLI:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Command
     - Description
   * - ``nipyapi ci list_nars``
     - List all installed NARs (JSON output)
   * - ``nipyapi ci upload_nar --nar_file <path>``
     - Upload and install a NAR
   * - ``nipyapi ci delete_nar --identifier <id>``
     - Delete a NAR by identifier
   * - ``nipyapi ci delete_nar --group_id <g> --artifact_id <a> --version <v>``
     - Delete a NAR by coordinates

Testing with Generated NARs
===========================

For integration testing, NiPyAPI includes a utility to programmatically generate minimal
Python processor NARs without requiring external build tools.

.. code-block:: python

    from tests.conftest import create_test_nar
    import nipyapi

    # Create a valid NAR with a recognizable processor
    nar_path = create_test_nar(version="0.0.1", processor_name="MyTestProcessor")
    nar = nipyapi.extensions.upload_nar(nar_path)

    # Verify processor is recognized
    details = nipyapi.extensions.get_nar_details(nar.identifier)
    assert len(details.processor_types) == 1

    # Cleanup
    nipyapi.extensions.delete_nar(nar.identifier)

    # Create an "invalid" NAR (uploads but has no processor types)
    invalid_path = create_test_nar(version="0.0.1", valid=False)
    invalid_nar = nipyapi.extensions.upload_nar(invalid_path)
    invalid_details = nipyapi.extensions.get_nar_details(invalid_nar.identifier)
    assert len(invalid_details.processor_types or []) == 0  # No processors!

**Parameters:**

- ``version``: The ProcessorDetails.version value (e.g., "0.0.1" or "0.0.1-SNAPSHOT")
- ``processor_name``: Name of the processor class (default: "NipyapiTestProcessor")
- ``valid``: If True (default), include Java implements declaration so NiFi recognizes the
  processor. If False, omit it to test invalid NAR handling.

**Use Cases:**

- Testing multi-version workflows without external NAR build process
- Testing NAR upload/delete operations
- Testing error handling for invalid NAR content
- CI/CD pipeline testing without binary artifacts

Troubleshooting
===============

Processor Stuck in "Initializing"
---------------------------------

**Symptoms:**

- Processor shows "Initializing runtime environment" for extended periods
- Properties never load

**Possible Causes:**

1. Network issues preventing dependency downloads
2. Large dependencies taking time to download
3. PyPI or custom package index is slow or unavailable

**Solutions:**

1. Verify network connectivity to PyPI from the NiFi cluster
2. Check NiFi logs for pip/download errors
3. Consider bundling dependencies in the NAR for air-gapped deployments

Dependency Download Failed
--------------------------

**Symptoms:**

- Processor cycles between "downloading" and "failed" states
- ``get_processor_init_status()`` returns ``status: dependency_failed``
- Properties never load

**Possible Causes:**

1. No network access to PyPI
2. Required packages don't exist or have version conflicts
3. Custom package index is misconfigured

**Solutions:**

1. Ensure cluster has network access to download packages
2. Verify dependency specifications in the processor's ``ProcessorDetails``
3. Bundle all dependencies in the NAR file

"Missing Processor" Error
-------------------------

**Symptoms:**

- Processor shows "Missing Processor" validation error
- Processor type not recognized

**Cause:**

The NAR containing this processor type has been removed.

**Solutions:**

1. Re-upload the NAR to recover the component
2. Delete the orphaned processor if no longer needed

Cannot Delete NAR
-----------------

**Symptoms:**

- Delete operation fails with "components are instantiated" error

**Cause:**

Components (processors, controller services) are using the NAR.

**Solutions:**

1. Delete or stop all components using the NAR first
2. Use ``force=True`` to orphan components (not recommended for production)

To find components using a NAR:

.. code-block:: python

    import nipyapi

    details = nipyapi.extensions.get_nar_details(nar_id)
    proc_types = [p.type for p in details.processor_types]
    print(f"Processor types from this NAR: {proc_types}")

Python Code Compilation Errors
------------------------------

**Symptoms:**

- NAR uploads successfully but processor fails validation
- Processor type not recognized after NAR installation
- Component deployment fails with unclear errors

**Cause:**

The Python code in the NAR has syntax errors or import failures that prevent NiFi from loading
the processor class. Common issues include:

- Syntax errors in the Python source
- Missing imports or undefined references
- Incompatible Python version (processors require Python 3.9-3.12)
- Missing ``__init__.py`` in package directories

**Solutions:**

1. Check NiFi application logs (``$NIFI_HOME/logs/nifi-app.log``) for Python errors
2. Look for stack traces mentioning the processor class name
3. Verify the processor code runs locally before packaging
4. Ensure all module dependencies are correctly specified

**Example log entries to look for:**

.. code-block:: text

    ERROR [...] Failed to load Python processor: MyProcessor
    SyntaxError: invalid syntax
    ImportError: No module named 'some_dependency'

Processor Type Not Recognized
-----------------------------

**Symptoms:**

- NAR uploads successfully and shows "Installed" state
- ``get_nar_details()`` returns empty ``processor_types`` list
- Processor type does not appear in NiFi's processor list

**Cause:**

Python processors require a specific ``class Java`` declaration for NiFi to recognize them as
valid processor types. Without this declaration, the NAR uploads successfully but contains
no discoverable processors.

**Required Structure:**

.. code-block:: python

    from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

    class MyProcessor(FlowFileTransform):
        # This declaration is REQUIRED for NiFi to recognize the processor
        class Java:
            implements = ['org.apache.nifi.python.processor.FlowFileTransform']

        class ProcessorDetails:
            version = '1.0.0-SNAPSHOT'
            description = 'My processor description'
            tags = ['example']
            dependencies = []

        def __init__(self, **kwargs):
            super().__init__()

        def transform(self, context, flow_file):
            return FlowFileTransformResult(relationship="success")

**Key Points:**

- The ``class Java: implements = [...]`` declaration tells NiFi this is a valid processor
- Without it, the NAR is structurally valid but has no processor types
- The implements value must match the processor's base class:

  - ``FlowFileTransform`` -> ``org.apache.nifi.python.processor.FlowFileTransform``
  - ``FlowFileSource`` -> ``org.apache.nifi.python.processor.FlowFileSource``
  - ``RecordTransform`` -> ``org.apache.nifi.python.processor.RecordTransform``

**Verification:**

.. code-block:: python

    import nipyapi

    nar = nipyapi.extensions.upload_nar("/path/to/my-processor.nar")
    details = nipyapi.extensions.get_nar_details(nar.identifier)

    if not details.processor_types:
        print("ERROR: NAR has no processor types - check Java implements declaration")
    else:
        for pt in details.processor_types:
            print(f"Found: {pt.type} (version: {pt.bundle.version})")

NAR Installation Timeout
------------------------

**Symptoms:**

- ``upload_nar()`` times out
- NAR state stuck at "Installing"

**Possible Causes:**

1. Large NAR file
2. Cluster under heavy load
3. Installation failed silently

**Solutions:**

1. Increase timeout: ``upload_nar(path, timeout=300)``
2. Check NAR state manually:

.. code-block:: python

    nar = nipyapi.extensions.get_nar(identifier)
    print(f"State: {nar.state}")
    print(f"Complete: {nar.install_complete}")
    print(f"Failure: {nar.failure_message}")
