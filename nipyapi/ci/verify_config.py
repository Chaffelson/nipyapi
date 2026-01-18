# pylint: disable=duplicate-code
"""
verify_config - verify configuration of components before starting a flow.
"""

import logging
import os
from typing import Any, Dict, List, Optional

import nipyapi

log = logging.getLogger(__name__)


def _verify_single_controller(controller) -> Dict[str, Any]:
    """Verify a single controller service and return result dict."""
    base_result = {
        "id": controller.id,
        "name": controller.component.name,
        "type": controller.component.type,
    }

    # Skip if not disabled
    if controller.component.state != "DISABLED":
        log.debug(
            "Skipping controller %s (state: %s)",
            controller.component.name,
            controller.component.state,
        )
        return {
            **base_result,
            "skipped": True,
            "reason": f"State is {controller.component.state}, not DISABLED",
        }

    log.info("Verifying controller: %s", controller.component.name)
    try:
        results = nipyapi.canvas.verify_controller(controller)
        failures = [r for r in results if r.outcome == "FAILED"]
        return {
            **base_result,
            "success": len(failures) == 0,
            "failures": [
                {"step": f.verification_step_name, "explanation": f.explanation} for f in failures
            ],
        }
    except Exception as e:  # pylint: disable=broad-except
        log.error("Error verifying controller %s: %s", controller.component.name, str(e))
        return {**base_result, "success": False, "error": str(e)}


def _verify_single_processor(processor) -> Dict[str, Any]:
    """Verify a single processor and return result dict."""
    base_result = {
        "id": processor.id,
        "name": processor.component.name,
        "type": processor.component.type,
    }

    # Skip if running
    run_status = processor.status.run_status if processor.status else "Unknown"
    if run_status.upper() in ("RUNNING", "VALIDATING"):
        log.debug("Skipping processor %s (state: %s)", processor.component.name, run_status)
        return {**base_result, "skipped": True, "reason": f"State is {run_status}, not stopped"}

    log.info("Verifying processor: %s", processor.component.name)
    try:
        results = nipyapi.canvas.verify_processor(processor)
        failures = [r for r in results if r.outcome == "FAILED"]
        return {
            **base_result,
            "success": len(failures) == 0,
            "failures": [
                {"step": f.verification_step_name, "explanation": f.explanation} for f in failures
            ],
        }
    except Exception as e:  # pylint: disable=broad-except
        log.error("Error verifying processor %s: %s", processor.component.name, str(e))
        return {**base_result, "success": False, "error": str(e)}


def _verify_controllers(process_group_id: str) -> List[Dict[str, Any]]:
    """Verify all controller services in a process group."""
    controllers = nipyapi.canvas.list_all_controllers(process_group_id, descendants=False)
    log.debug("Found %d controller services", len(controllers))
    return [_verify_single_controller(c) for c in controllers]


def _verify_processors(process_group_id: str) -> List[Dict[str, Any]]:
    """Verify all processors in a process group and its descendants."""
    processors = nipyapi.canvas.list_all_processors(process_group_id)
    log.debug("Found %d processors in PG and descendants", len(processors))
    return [_verify_single_processor(p) for p in processors]


def verify_config(
    process_group_id: Optional[str] = None,
    verify_controllers: bool = True,
    verify_processors: bool = True,
    only_failures: bool = False,
) -> dict:
    """
    Verify configuration of all components in a process group.

    Validates that all required properties are set and property values meet
    their defined constraints. Does NOT test actual connectivity or credentials.
    Designed for CI/CD pipelines to catch configuration errors before starting
    a flow. Verifies controller services and processors that are in a
    stopped/disabled state.

    Args:
        process_group_id: ID of the process group. Env: NIFI_PROCESS_GROUP_ID
        verify_controllers: Verify controller services (default: True)
        verify_processors: Verify processors (default: True)
        only_failures: Only include failed components in results (default: False).
            When True, controller_results and processor_results contain only
            items with success=False. Reduces output size for large process groups.

    Returns:
        dict with keys: verified ("true"/"false"), failed_count,
        controller_results, processor_results, summary, and process_group_name.
        When only_failures=True, also includes controllers_checked and
        processors_checked counts.
        Caller should check verified or failed_count to determine next steps.

    Raises:
        ValueError: Missing required parameters or process group not found

    Example::

        # CLI usage
        nipyapi ci verify_config --process-group-id <pg-id>

        # Only show failures (cleaner output for large flows)
        nipyapi ci verify_config --process-group-id <pg-id> --only_failures

        # Programmatic usage
        result = nipyapi.ci.verify_config(process_group_id)
        if result["verified"] == "true":
            nipyapi.ci.start_flow(process_group_id)
        else:
            print(f"Verification failed: {result['summary']}")
    """
    process_group_id = process_group_id or os.environ.get("NIFI_PROCESS_GROUP_ID")
    if not process_group_id:
        raise ValueError("process_group_id is required (or set NIFI_PROCESS_GROUP_ID)")

    log.info("Verifying configuration for process group: %s", process_group_id)

    process_group = nipyapi.canvas.get_process_group(process_group_id, "id")
    if not process_group:
        raise ValueError(f"Process group not found: {process_group_id}")
    log.debug("Found process group: %s", process_group.component.name)

    # Verify components
    controller_results = _verify_controllers(process_group_id) if verify_controllers else []
    processor_results = _verify_processors(process_group_id) if verify_processors else []
    all_results = controller_results + processor_results

    # Count and log failures (results with success=False, excluding skipped)
    failed_count = sum(1 for r in all_results if r.get("success") is False)
    for r in all_results:
        if r.get("success") is False:
            log.warning("%s verification FAILED", r["name"])

    # Build summary
    total_verified = len(all_results)
    summary = (
        f"All {total_verified} components passed verification"
        if failed_count == 0
        else f"{total_verified - failed_count}/{total_verified} passed, {failed_count} failed"
    )
    log.info("Verification complete: %s", summary)

    # Build result with optional filtering
    result = {
        "verified": "true" if failed_count == 0 else "false",
        "failed_count": failed_count,
        "controller_results": (
            [r for r in controller_results if r.get("success") is False]
            if only_failures
            else controller_results
        ),
        "processor_results": (
            [r for r in processor_results if r.get("success") is False]
            if only_failures
            else processor_results
        ),
        "summary": summary,
        "process_group_name": process_group.component.name,
    }

    # Add checked counts when filtering (so caller knows the scope)
    if only_failures:
        result["controllers_checked"] = len(controller_results)
        result["processors_checked"] = len(processor_results)

    # Add error key for CLI exit code detection when verification fails
    if failed_count > 0:
        result["error"] = "Verification failed for: {}".format(
            ", ".join(r["name"] for r in all_results if r.get("success") is False)
        )

    return result
