"""Upload an asset to a parameter context."""

import logging
import os
import urllib.request
from typing import Optional

import nipyapi

log = logging.getLogger(__name__)


# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
# pylint: disable=too-many-branches,too-many-statements
def upload_asset(
    process_group_id: Optional[str] = None,
    context_id: Optional[str] = None,
    file_path: Optional[str] = None,
    url: Optional[str] = None,
    filename: Optional[str] = None,
    param_name: Optional[str] = None,
) -> dict:
    """
    Upload an asset and optionally link it to a parameter.

    This function uploads a file (from local path or URL) as an asset to a
    parameter context, and can optionally update a parameter to reference it.

    Args:
        process_group_id: Process group to find parameter context from.
            Env: NIFI_PROCESS_GROUP_ID
        context_id: Direct parameter context ID (alternative to process_group_id).
            Env: NIFI_PARAMETER_CONTEXT_ID
        file_path: Path to local file to upload.
            Env: NIFI_ASSET_FILE_PATH
        url: URL to download file from (alternative to file_path).
            Env: NIFI_ASSET_URL
        filename: Override the filename (defaults to basename from path/URL).
            Env: NIFI_ASSET_FILENAME
        param_name: If provided, update this parameter to reference the asset.
            Env: NIFI_ASSET_PARAM_NAME

    Returns:
        dict with:
            - asset_id: ID of the uploaded asset
            - asset_name: Name of the uploaded asset
            - asset_digest: SHA-256 digest of the asset
            - context_id: Parameter context the asset was uploaded to
            - context_name: Name of the parameter context
            - parameter_updated: "true" if param_name was provided and updated

    Raises:
        ValueError: Missing required parameters or file not found

    Example:
        # Upload from URL and link to parameter
        nipyapi ci upload_asset \\
            --url https://jdbc.postgresql.org/download/postgresql-42.7.6.jar \\
            --context_id abc123 \\
            --param_name "PostgreSQL JDBC Driver"

        # Upload from file path
        nipyapi ci upload_asset \\
            --file_path /path/to/driver.jar \\
            --process_group_id def456
    """
    # Get from environment if not provided
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    context_id = context_id or os.environ.get("NIFI_PARAMETER_CONTEXT_ID")
    file_path = file_path or os.environ.get("NIFI_ASSET_FILE_PATH")
    url = url or os.environ.get("NIFI_ASSET_URL")
    filename = filename or os.environ.get("NIFI_ASSET_FILENAME")
    param_name = param_name or os.environ.get("NIFI_ASSET_PARAM_NAME")

    # Validate inputs
    if not process_group_id and not context_id:
        raise ValueError(
            "Either process_group_id or context_id is required "
            "(or set NIFI_PROCESS_GROUP_ID or NIFI_PARAMETER_CONTEXT_ID)"
        )

    if not file_path and not url:
        raise ValueError(
            "Either file_path or url is required "
            + "(or set NIFI_ASSET_FILE_PATH or NIFI_ASSET_URL)"
        )

    nipyapi.profiles.switch()

    # Resolve context ID from process group if needed
    context_name = None
    if context_id is None:
        log.info("Finding parameter context from process group %s", process_group_id)
        pg = nipyapi.canvas.get_process_group(process_group_id, identifier_type="id")
        if pg is None:
            raise ValueError(f"Process group not found: {process_group_id}")
        if not pg.component.parameter_context:
            raise ValueError(f"Process group '{pg.component.name}' has no parameter context")
        context_id = pg.component.parameter_context.id
        context_name = pg.component.parameter_context.component.name
        log.info("Using parameter context: %s (%s)", context_name, context_id)
    else:
        # Get context name for output
        ctx = nipyapi.parameters.get_parameter_context(context_id, identifier_type="id")
        if ctx is None:
            raise ValueError(f"Parameter context not found: {context_id}")
        context_name = ctx.component.name

    # Get file content
    file_bytes = None
    if url:
        log.info("Downloading from URL: %s", url)
        try:
            with urllib.request.urlopen(url) as response:
                file_bytes = response.read()
            if filename is None:
                # Extract filename from URL
                filename = url.split("/")[-1].split("?")[0]
            log.info("Downloaded %d bytes as %s", len(file_bytes), filename)
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise ValueError(f"Failed to download from URL: {e}") from e
    elif file_path:
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")
        log.info("Reading from file: %s", file_path)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        if filename is None:
            filename = os.path.basename(file_path)
        log.info("Read %d bytes from %s", len(file_bytes), file_path)

    # Upload the asset
    log.info("Uploading asset '%s' to context %s", filename, context_id)
    asset = nipyapi.parameters.upload_asset(
        context_id=context_id, file_bytes=file_bytes, filename=filename
    )
    log.info("Uploaded asset: %s (%s)", asset["name"], asset["id"])

    result = {
        "asset_id": asset["id"],
        "asset_name": asset["name"],
        "asset_digest": asset["digest"],
        "context_id": context_id,
        "context_name": context_name,
        "parameter_updated": "false",
    }

    # Optionally update parameter to reference the asset
    if param_name:
        log.info("Updating parameter '%s' to reference asset", param_name)

        # Get context for update
        ctx = nipyapi.parameters.get_parameter_context(context_id, identifier_type="id")

        # Prepare parameter with asset reference
        param = nipyapi.parameters.prepare_parameter_with_asset(
            name=param_name, asset_id=asset["id"], asset_name=asset["name"]
        )

        # Update the parameter
        nipyapi.parameters.upsert_parameter_to_context(ctx, param)
        log.info("Updated parameter '%s' to reference '%s'", param_name, asset["name"])
        result["parameter_updated"] = "true"
        result["parameter_name"] = param_name

    return result
