"""
NiFi Extensions (NAR) Management Module.

Provides functions for managing custom NAR files (extensions) in NiFi.
NAR files contain custom processors, controller services, and other components.

NAR Functions:
    - upload_nar() - Upload a NAR file and wait for installation
    - list_nars() - List all installed NARs
    - get_nar() - Get summary of a specific NAR
    - get_nar_details() - Get component types in a NAR
    - get_nar_by_coordinate() - Find NAR by Maven coordinate
    - download_nar() - Download a NAR file
    - delete_nar() - Remove an installed NAR

Processor Initialization Functions:
    - get_processor_init_status() - Get initialization status of extension processor
    - wait_for_processor_init() - Wait for extension processor to initialize

Processor Bundle Version Functions:
    - get_processor_bundle_versions() - List available versions for a processor type
    - get_processor_type_version() - Get processor type for a specific bundle version
    - change_processor_bundle_version() - Change processor to a different bundle version

Python processors and other extension processors may require initialization time
after being created (e.g., setting up a virtual environment). Use the processor
initialization functions to detect and wait for this.

Example::

    >>> import nipyapi
    >>> # Upload a NAR and create a processor
    >>> nar = nipyapi.extensions.upload_nar('/path/to/custom.nar')
    >>> details = nipyapi.extensions.get_nar_details(nar.identifier)
    >>> proc_type = nipyapi.canvas.get_processor_type(details.processor_types[0].type)
    >>> proc = nipyapi.canvas.create_processor(pg, proc_type, (0,0), 'MyProc')
    >>> # Wait for Python processor to initialize
    >>> proc = nipyapi.extensions.wait_for_processor_init(proc)
"""

import logging
import os

import nipyapi

log = logging.getLogger(__name__)


def list_nars():
    """
    List all installed NARs in NiFi.

    Returns:
        list[:class:`~nipyapi.nifi.models.NarSummaryDTO`]: List of NAR summary objects

    Example::

        >>> nars = nipyapi.extensions.list_nars()
        >>> for nar in nars:
        ...     print(f"{nar.coordinate.group}:{nar.coordinate.artifact}")
    """
    with nipyapi.utils.rest_exceptions():
        response = nipyapi.nifi.ControllerApi().get_nar_summaries()

    if not response.nar_summaries:
        return []

    return [entity.nar_summary for entity in response.nar_summaries]


def get_nar(identifier):
    """
    Get summary of a specific NAR by its identifier.

    Args:
        identifier (str): The NAR identifier (UUID)

    Returns:
        :class:`~nipyapi.nifi.models.NarSummaryDTO`: NAR summary object,
            or None if not found

    Example::

        >>> nar = nipyapi.extensions.get_nar('abc-123-def')
        >>> print(nar.state)
    """
    with nipyapi.utils.rest_exceptions():
        try:
            response = nipyapi.nifi.ControllerApi().get_nar_summary(identifier)
            return response.nar_summary
        except nipyapi.nifi.rest.ApiException as e:
            if e.status == 404:
                return None
            raise


def get_nar_details(identifier):
    """
    Get component types contained in a NAR.

    Args:
        identifier (str): The NAR identifier (UUID)

    Returns:
        :class:`~nipyapi.nifi.models.NarDetailsEntity`: NAR details with
            processor_types, controller_service_types, reporting_task_types.
            Returns None if not found.

    Example::

        >>> details = nipyapi.extensions.get_nar_details('abc-123-def')
        >>> for proc in details.processor_types:
        ...     print(proc.type)
    """
    with nipyapi.utils.rest_exceptions():
        try:
            return nipyapi.nifi.ControllerApi().get_nar_details(identifier)
        except nipyapi.nifi.rest.ApiException as e:
            if e.status == 404:
                return None
            raise


def get_nar_by_coordinate(group, artifact, version=None):
    """
    Find a NAR by its Maven coordinate.

    Args:
        group (str): Maven group ID (e.g., 'com.example')
        artifact (str): Maven artifact ID (e.g., 'my-processors-nar')
        version (str, optional): Specific version. If None, returns all versions.

    Returns:
        :class:`~nipyapi.nifi.models.NarSummaryDTO` or list: Single NAR if version
            specified, list of matching NARs otherwise. Returns None if not found.

    Example::

        >>> nar = nipyapi.extensions.get_nar_by_coordinate(
        ...     'com.example', 'my-processors-nar', '1.0.0'
        ... )
    """
    nars = list_nars()
    matches = []

    for nar in nars:
        coord = nar.coordinate
        if coord and coord.group == group and coord.artifact == artifact:
            if version is None or coord.version == version:
                matches.append(nar)

    if version is not None:
        return matches[0] if matches else None
    return matches if matches else None


def upload_nar(file_path=None, file_bytes=None, filename=None, timeout=120):
    """
    Upload a NAR file to NiFi and wait for installation to complete.

    This function performs a two-phase wait. First, it waits for the NAR to
    reach INSTALLED state. Then, for NARs with extensions (especially Python
    processors), it waits for processor types to be discovered in the API.
    The discovery phase is important because processor type discovery happens
    asynchronously after the NAR is marked as installed.

    Args:
        file_path (str, optional): Path to NAR file on disk
        file_bytes (bytes, optional): NAR file contents as bytes
        filename (str, optional): Filename for the NAR. Required if using file_bytes,
            defaults to basename of file_path otherwise.
        timeout (int): Maximum seconds to wait for both phases (default: 120)

    Returns:
        :class:`~nipyapi.nifi.models.NarSummaryDTO`: Installed NAR summary

    Raises:
        ValueError: If neither file_path nor file_bytes provided, or installation fails
        FileNotFoundError: If file_path doesn't exist

    Example::

        >>> nar = nipyapi.extensions.upload_nar('/path/to/my-nar-1.0.0.nar')
        >>> print(f"Installed: {nar.identifier}")
        >>> # Processor types are now available
        >>> details = nipyapi.extensions.get_nar_details(nar.identifier)
        >>> print(f"Processors: {len(details.processor_types)}")
    """
    if file_path is None and file_bytes is None:
        raise ValueError("Either file_path or file_bytes must be provided")

    if file_path is not None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"NAR file not found: {file_path}")
        if filename is None:
            filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
    elif filename is None:
        raise ValueError("filename is required when using file_bytes")

    log.info("Uploading NAR: %s (%d bytes)", filename, len(file_bytes))

    with nipyapi.utils.rest_exceptions():
        response = nipyapi.nifi.ControllerApi().upload_nar(body=file_bytes, filename=filename)

    nar_id = response.nar_summary.identifier
    log.info("NAR uploaded: %s, waiting for installation...", nar_id)

    # Wait for installation to complete
    result = nipyapi.utils.wait_to_complete(
        _check_nar_install_complete,
        nar_id,
        nipyapi_delay=2,
        nipyapi_max_wait=timeout,
    )

    log.info("NAR installed: %s (extensions: %d)", nar_id, result.extension_count or 0)
    return result


def download_nar(identifier, file_path=None):
    """
    Download a NAR file from NiFi.

    Args:
        identifier (str): The NAR identifier
        file_path (str, optional): Path to write the NAR file. If None, returns bytes.

    Returns:
        bytes or str: NAR file contents if file_path is None, otherwise the file path

    Example::

        >>> nipyapi.extensions.download_nar('abc-123', '/tmp/backup.nar')
        >>> # Or get bytes directly
        >>> nar_bytes = nipyapi.extensions.download_nar('abc-123')
    """
    with nipyapi.utils.rest_exceptions():
        # Use _preload_content=False to get raw binary response
        # The generated client tries to decode as UTF-8 which fails for binary
        response = nipyapi.nifi.ControllerApi().download_nar(identifier, _preload_content=False)
        # Read the raw binary data from the response
        nar_bytes = response.read()

    if file_path:
        with open(file_path, "wb") as f:
            f.write(nar_bytes)
        log.info("Downloaded NAR to: %s", file_path)
        return file_path

    return nar_bytes


def delete_nar(identifier, force=False, timeout=30):
    """
    Delete an installed NAR from NiFi and wait for cleanup to complete.

    When force=True, waits for the NAR to be removed and any processors using
    it to reach a halting state (deleted, orphaned/missing_nar, or error).

    Warning: If force=True and processors from this NAR are still initializing
    (e.g., Python venv creation in progress), the NiFi API will block. This
    function checks for initializing processors and raises an error to prevent
    this. See resources/scripts/NIFI_PYTHON_BRIDGE_BUGS.md for details.

    Args:
        identifier (str): The NAR identifier
        force (bool): Force deletion even if components are in use
        timeout (int): Maximum seconds to wait for cleanup (default: 30)

    Returns:
        dict with keys: nar_summary, cleanup_complete, and affected_processors.

    Raises:
        ValueError: If force=True and processors from this NAR are still
            initializing. Delete the processors first or wait for them
            to complete initialization.

    Example::

        >>> result = nipyapi.extensions.delete_nar('abc-123-def', force=True)
        >>> if result['cleanup_complete']:
        ...     print("NAR and all processors cleaned up")
    """
    log.info("Deleting NAR: %s (force=%s)", identifier, force)

    # Check for initializing processors to avoid NiFi API blocking bug
    if force:
        initializing_procs = _get_initializing_processors_for_nar(identifier)
        if initializing_procs:
            proc_names = [p.component.name for p in initializing_procs]
            raise ValueError(
                f"Cannot force delete NAR while processors are initializing: {proc_names}. "
                "NiFi's delete API may block indefinitely during processor initialization. "
                "Either wait for initialization to complete using "
                "wait_for_processor_init(), or delete the processors first."
            )

    # Track affected processors before deletion (for force=True cleanup verification)
    affected_proc_ids = []
    if force:
        affected_proc_ids = _get_processor_ids_for_nar(identifier)
        log.debug("Tracking %d processors for cleanup verification", len(affected_proc_ids))

    # Execute deletion
    with nipyapi.utils.rest_exceptions():
        response = nipyapi.nifi.ControllerApi().delete_nar(identifier, force=force)

    nar_summary = response.nar_summary
    log.info("NAR delete API completed: %s", identifier)

    # Wait for system to reach stable state
    cleanup_complete = True
    if force and affected_proc_ids:
        cleanup_complete = _wait_for_nar_cleanup(identifier, affected_proc_ids, timeout)

    return {
        "nar_summary": nar_summary,
        "cleanup_complete": cleanup_complete,
        "affected_processors": affected_proc_ids,
    }


def _get_processor_ids_for_nar(nar_identifier):
    """
    Get IDs of all processors currently using a NAR.

    Args:
        nar_identifier (str): The NAR identifier

    Returns:
        list: Processor ID strings
    """
    try:
        details = get_nar_details(nar_identifier)
        if not details or not details.processor_types:
            return []

        # Get processor type names from this NAR
        nar_proc_types = {pt.type for pt in details.processor_types}

        # Get all processors in the flow
        root_pg = nipyapi.canvas.get_process_group("root", "name")
        all_procs = nipyapi.canvas.list_all_processors(root_pg.id)

        # Find processors that match NAR types
        matching_ids = []
        for proc in all_procs:
            if proc.component.type in nar_proc_types:
                matching_ids.append(proc.id)

        return matching_ids
    except (AttributeError, TypeError, nipyapi.nifi.rest.ApiException) as e:
        log.warning("Could not get processors for NAR: %s", e)
        return []


def _wait_for_nar_cleanup(nar_identifier, affected_proc_ids, timeout):
    """
    Wait for NAR deletion cleanup to complete.

    Polls until:
    - The NAR is no longer found in the system
    - All affected processors have reached a halting state

    Args:
        nar_identifier (str): The NAR identifier (to verify it's gone)
        affected_proc_ids (list): Processor IDs to check
        timeout (int): Maximum seconds to wait

    Returns:
        bool: True if cleanup completed, False if timeout reached
    """
    halting_states = {"missing_nar", "error"}

    def _check_cleanup_complete():
        # Verify NAR is gone
        if get_nar(nar_identifier) is not None:
            log.debug("NAR still exists, waiting...")
            return False

        # Check each affected processor
        for proc_id in affected_proc_ids:
            proc = nipyapi.canvas.get_processor(proc_id, "id")
            if proc is None:
                # Processor was deleted by NiFi, that's a halting state
                continue

            status = get_processor_init_status(proc)
            if status["status"] not in halting_states:
                log.debug(
                    "Processor %s in state '%s', waiting for halting state...",
                    proc_id,
                    status["status"],
                )
                return False

        return True

    try:
        nipyapi.utils.wait_to_complete(
            _check_cleanup_complete,
            nipyapi_delay=0.5,
            nipyapi_max_wait=timeout,
        )
        log.info("NAR cleanup complete: %s", nar_identifier)
        return True
    except ValueError:
        # Timeout reached - return gracefully with incomplete cleanup
        log.warning(
            "NAR cleanup did not complete within %ds for %s",
            timeout,
            nar_identifier,
        )
        return False


def _get_initializing_processors_for_nar(nar_identifier):
    """
    Find any processors from a NAR that are still initializing.

    Args:
        nar_identifier (str): The NAR identifier

    Returns:
        list: ProcessorEntity objects that are still initializing
    """
    try:
        details = get_nar_details(nar_identifier)
        if not details or not details.processor_types:
            return []

        # Get processor type names from this NAR
        nar_proc_types = {pt.type for pt in details.processor_types}

        # Get all processors in the flow
        root_pg = nipyapi.canvas.get_process_group("root", "name")
        all_procs = nipyapi.canvas.list_all_processors(root_pg.id)

        # Find processors that match NAR types and are initializing
        initializing = []
        for proc in all_procs:
            if proc.component.type in nar_proc_types:
                status = get_processor_init_status(proc)
                if status["status"] in ("initializing", "downloading_dependencies"):
                    initializing.append(proc)

        return initializing
    except (AttributeError, TypeError, nipyapi.nifi.rest.ApiException) as e:
        # If we can't check (NAR not found, API error, etc.), proceed cautiously
        log.warning("Could not check for initializing processors: %s", e)
        return []


def get_processor_init_status(processor):
    """
    Get the initialization status of a processor from a custom NAR.

    Python processors and other extension processors may require initialization
    time after being created (e.g., setting up a virtual environment).

    Args:
        processor: ProcessorEntity or processor ID string

    Returns:
        dict with:
            - status: One of 'initializing', 'downloading_dependencies',
              'dependency_failed', 'ready', 'missing_nar', or 'error'
            - is_ready: True if processor is fully initialized
            - has_properties: True if properties are loaded
            - validation_status: The processor's validation_status field
            - validation_errors: List of validation error strings
            - init_message: Human-readable description of current state

    Example::

        >>> status = nipyapi.extensions.get_processor_init_status(proc)
        >>> if status['is_ready']:
        ...     print("Processor ready for configuration")
    """
    # Get processor if ID provided
    if isinstance(processor, str):
        processor = nipyapi.canvas.get_processor(processor, "id")

    if processor is None:
        return {
            "status": "error",
            "is_ready": False,
            "has_properties": False,
            "validation_status": None,
            "validation_errors": [],
            "init_message": "Processor not found",
        }

    errors = processor.component.validation_errors or []
    props = processor.component.config.properties if processor.component.config else {}
    has_properties = bool(props)
    validation_status = processor.component.validation_status

    # Check for specific error patterns
    is_initializing = any("Initializing" in str(e) for e in errors)
    is_missing_nar = any("Missing Processor" in str(e) for e in errors)
    is_downloading = any("downloading third-party" in str(e).lower() for e in errors)
    is_download_failed = any("Failed to download" in str(e) for e in errors)

    # Determine status
    if is_missing_nar:
        status = "missing_nar"
        init_message = "NAR has been removed - processor is orphaned"
    elif is_download_failed:
        status = "dependency_failed"
        init_message = "Failed to download dependencies - check EAI/network access"
    elif is_downloading:
        status = "downloading_dependencies"
        init_message = "Downloading third-party dependencies from PyPI"
    elif is_initializing:
        status = "initializing"
        init_message = "Runtime environment is being initialized"
    else:
        # If no initialization-related errors are present, the processor is ready.
        # A processor can legitimately have no user-defined properties.
        status = "ready"
        init_message = "Processor initialized and ready for configuration"

    return {
        "status": status,
        "is_ready": status == "ready",
        "has_properties": has_properties,
        "validation_status": validation_status,
        "validation_errors": errors,
        "init_message": init_message,
    }


def wait_for_processor_init(processor, timeout=60):
    """
    Wait for a processor from a custom NAR to complete initialization.

    Python processors need time to set up their virtual environment after
    being created. This function waits until the processor is ready.

    Args:
        processor: ProcessorEntity or processor ID string
        timeout (int): Maximum seconds to wait (default: 60)

    Returns:
        :class:`~nipyapi.nifi.models.ProcessorEntity`: The initialized processor

    Raises:
        ValueError: If processor not found, NAR missing, dependency download
            failed, or timeout reached

    Example::

        >>> proc = nipyapi.canvas.create_processor(...)
        >>> proc = nipyapi.extensions.wait_for_processor_init(proc)
        >>> # Processor is now ready for configuration
    """
    # Get processor ID
    if isinstance(processor, str):
        proc_id = processor
    else:
        proc_id = processor.id

    log.info("Waiting for processor initialization: %s (timeout=%ds)", proc_id, timeout)

    def _check_processor_ready(processor_id):
        status = get_processor_init_status(processor_id)

        log.debug(
            "Processor %s status: %s, has_props: %s",
            processor_id,
            status["status"],
            status["has_properties"],
        )

        if status["status"] == "missing_nar":
            raise ValueError(f"NAR missing for processor {processor_id}")

        if status["status"] == "dependency_failed":
            raise ValueError(
                f"Dependency download failed for processor {processor_id}. "
                "Check EAI configuration for PyPI access."
            )

        # Continue waiting for initialization states
        if status["status"] in ("initializing", "downloading_dependencies"):
            return False

        if status["is_ready"]:
            return nipyapi.canvas.get_processor(processor_id, "id")

        return False

    result = nipyapi.utils.wait_to_complete(
        _check_processor_ready,
        proc_id,
        nipyapi_delay=0.5,
        nipyapi_max_wait=timeout,
    )

    log.info("Processor initialized: %s", proc_id)
    return result


def get_processor_bundle_versions(processor_type):
    """
    List available bundle versions for a processor type.

    When multiple versions of the same processor type are installed (via
    multiple NARs), this function returns all available bundle versions.

    Args:
        processor_type (str): The processor type name (e.g., 'PrepareRegulatoryFile')
            or the full qualified type name

    Returns:
        list[dict]: List of available versions, each with:
            - bundle: BundleDTO with group, artifact, version
            - type: Full processor type name
            - description: Processor description

    Example::

        >>> versions = nipyapi.extensions.get_processor_bundle_versions(
        ...     'PrepareRegulatoryFile'
        ... )
        >>> for v in versions:
        ...     print(f"{v['bundle'].version}")
    """
    with nipyapi.utils.rest_exceptions():
        all_types = nipyapi.nifi.FlowApi().get_processor_types()

    matching = []
    for proc in all_types.processor_types:
        # Match by type name (either full or short name)
        if processor_type in proc.type:
            matching.append(
                {
                    "bundle": proc.bundle,
                    "type": proc.type,
                    "description": proc.description,
                }
            )

    return matching


def get_processor_type_version(processor_type, version):
    """
    Get a processor type with a specific bundle version for creation.

    When multiple versions of the same processor type are installed (via
    multiple NARs), use this function to get the correct type for creating
    a processor with a specific bundle version.

    Args:
        processor_type (str): The processor type name (e.g., 'PrepareRegulatoryFile')
        version (str): The bundle version (e.g., '0.0.2-SNAPSHOT')

    Returns:
        :class:`~nipyapi.nifi.models.DocumentedTypeDTO`: The processor type with
            the specified bundle version, suitable for passing to
            :func:`nipyapi.canvas.create_processor`

    Raises:
        ValueError: If no matching processor type/version found

    Example::

        >>> # Get the v2 processor type
        >>> proc_type = nipyapi.extensions.get_processor_type_version(
        ...     'PrepareRegulatoryFile', '0.0.2-SNAPSHOT'
        ... )
        >>> # Create processor with that specific version
        >>> proc = nipyapi.canvas.create_processor(pg, proc_type, (0,0), 'MyProc')
    """
    with nipyapi.utils.rest_exceptions():
        all_types = nipyapi.nifi.FlowApi().get_processor_types()

    for proc in all_types.processor_types:
        if processor_type in proc.type and proc.bundle.version == version:
            return proc

    # Not found - provide helpful error
    available = get_processor_bundle_versions(processor_type)
    if not available:
        raise ValueError(f"Processor type '{processor_type}' not found")

    available_versions = [v["bundle"].version for v in available]
    raise ValueError(
        f"Version '{version}' not available for {processor_type}. "
        f"Available: {available_versions}"
    )


def change_processor_bundle_version(processor, target_version):
    """
    Change a processor to use a different bundle version.

    When multiple versions of the same processor type are installed (via
    multiple NARs), this function allows changing which version an existing
    processor uses. This is different from versioned flow control - it changes
    the underlying processor implementation.

    Note: The processor must be stopped before changing versions.

    Args:
        processor: ProcessorEntity or processor ID string
        target_version (str): The target bundle version (e.g., '0.0.2-SNAPSHOT')
            or a BundleDTO object

    Returns:
        :class:`~nipyapi.nifi.models.ProcessorEntity`: The updated processor

    Raises:
        ValueError: If processor not found, or target version not available

    Example::

        >>> proc = nipyapi.canvas.get_processor('MyProcessor', 'name')
        >>> updated = nipyapi.extensions.change_processor_bundle_version(
        ...     proc, '0.0.2-SNAPSHOT'
        ... )
        >>> print(f"Now using: {updated.component.bundle.version}")
    """
    # Get processor if ID provided
    if isinstance(processor, str):
        processor = nipyapi.canvas.get_processor(processor, "id")

    if processor is None:
        raise ValueError("Processor not found")

    proc_type = processor.component.type
    current_bundle = processor.component.bundle

    log.info(
        "Changing processor %s from version %s to %s",
        processor.component.name,
        current_bundle.version,
        target_version if isinstance(target_version, str) else target_version.version,
    )

    # If target_version is a string, find the matching bundle
    if isinstance(target_version, str):
        available = get_processor_bundle_versions(proc_type)
        target_bundle = None
        for v in available:
            if v["bundle"].version == target_version:
                target_bundle = v["bundle"]
                break

        if target_bundle is None:
            available_versions = [v["bundle"].version for v in available]
            raise ValueError(
                f"Version '{target_version}' not available for {proc_type}. "
                f"Available: {available_versions}"
            )
    else:
        target_bundle = target_version

    # Get fresh processor entity for update
    processor = nipyapi.canvas.get_processor(processor.id, "id")

    # Update the bundle
    processor.component.bundle = target_bundle

    with nipyapi.utils.rest_exceptions():
        updated = nipyapi.nifi.ProcessorsApi().update_processor(
            id=processor.id,
            body=processor,
        )

    log.info(
        "Processor %s now using version %s",
        updated.component.name,
        updated.component.bundle.version,
    )

    return updated


def _check_nar_install_complete(identifier):
    """
    Check if a NAR installation is complete.

    Used internally by upload_nar with nipyapi.utils.wait_to_complete.

    This function checks two phases:
    1. Install phase: Wait for state == INSTALLED and install_complete == True
    2. Discovery phase: For NARs with extensions, wait for processor_types
       to be populated (Python processor discovery is async)

    Args:
        identifier (str): The NAR identifier

    Returns:
        NarSummaryDTO or False: NAR summary if installation complete, False otherwise

    Raises:
        ValueError: If NAR not found or installation failed
    """
    nar = get_nar(identifier)

    if nar is None:
        raise ValueError(f"NAR not found: {identifier}")

    state = str(nar.state or "UNKNOWN").upper()
    install_complete = nar.install_complete or False

    log.debug("NAR %s state: %s, complete: %s", identifier, state, install_complete)

    # Phase 1: Check install completion
    if state == "FAILED":
        failure_msg = nar.failure_message or "Unknown error"
        raise ValueError(f"NAR installation failed: {failure_msg}")

    if not install_complete or state != "INSTALLED":
        return False

    # Phase 2: Check processor discovery (for NARs that should have processors)
    # Python processor discovery is async and happens after install completes
    extension_count = nar.extension_count or 0

    if extension_count > 0:
        # NAR claims to have extensions - verify processor_types is populated
        details = get_nar_details(identifier)
        if details is None:
            log.debug("NAR %s: details not yet available", identifier)
            return False

        proc_count = len(details.processor_types) if details.processor_types else 0
        cs_count = len(details.controller_service_types) if details.controller_service_types else 0
        rt_count = len(details.reporting_task_types) if details.reporting_task_types else 0
        total_types = proc_count + cs_count + rt_count

        if total_types == 0:
            # Extensions reported but none discovered yet - still discovering
            log.debug(
                "NAR %s: extension_count=%d but no types discovered yet",
                identifier,
                extension_count,
            )
            return False

        log.debug(
            "NAR %s: discovered %d processor(s), %d controller service(s), %d reporting task(s)",
            identifier,
            proc_count,
            cs_count,
            rt_count,
        )

    return nar
