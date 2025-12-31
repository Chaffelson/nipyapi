#!/usr/bin/env python3
"""
Augmentation to fix ProcessorDTO.state enum.

Upstream NiFi bug: The 'state' field enum only includes stable states
["RUNNING", "STOPPED", "DISABLED"], but the API can return transitional
states like "RUN_ONCE", "STARTING", "STOPPING" (which are correctly
included in 'physicalState').

This augmentation updates the 'state' enum to match 'physicalState'.

Upstream issue: https://issues.apache.org/jira/browse/NIFI-15396
"""
import json
import sys


def fix_processor_dto_state(spec):
    """Update ProcessorDTO.state enum to include all processor states."""
    schemas = spec.get("components", {}).get("schemas", {})
    processor_dto = schemas.get("ProcessorDTO", {})
    properties = processor_dto.get("properties", {})

    # Get the complete enum from physicalState
    physical_state = properties.get("physicalState", {})
    complete_enum = physical_state.get("enum", [])

    if not complete_enum:
        # Fallback if physicalState doesn't exist
        complete_enum = [
            "RUNNING", "STOPPED", "DISABLED", "STARTING", "STOPPING", "RUN_ONCE"
        ]

    # Update state enum to match
    state_prop = properties.get("state", {})
    if state_prop and "enum" in state_prop:
        old_enum = state_prop["enum"]
        state_prop["enum"] = complete_enum
        print(f"  ProcessorDTO.state enum: {old_enum} -> {complete_enum}")

    return spec


def main():
    if len(sys.argv) != 3:
        print("Usage: nifi_processor_state_enum.py <input.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        spec = json.load(f)

    spec = fix_processor_dto_state(spec)

    with open(sys.argv[2], "w") as f:
        json.dump(spec, f, indent=2)


if __name__ == "__main__":
    main()
