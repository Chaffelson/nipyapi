#!/usr/bin/env python3
"""
Augmentation to fix AffectedComponentEntity.referenceType enum.

Upstream NiFi inconsistency: AffectedComponentDTO.referenceType allows
"STATELESS_GROUP", but AffectedComponentEntity.referenceType omits it, even
though NiFi returns it in the referencingComponents of parameter context
update requests and parameter provider apply requests.

This augmentation updates the entity enum to match the DTO enum.
"""
import json
import sys


def fix_affected_component_entity_reference_type(spec):
    """Update AffectedComponentEntity.referenceType enum to match the DTO."""
    schemas = spec.get("components", {}).get("schemas", {})
    dto_props = schemas.get("AffectedComponentDTO", {}).get("properties", {})
    complete_enum = dto_props.get("referenceType", {}).get("enum", [])

    if not complete_enum:
        # Fallback if the DTO enum is missing
        complete_enum = [
            "PROCESSOR",
            "CONTROLLER_SERVICE",
            "INPUT_PORT",
            "OUTPUT_PORT",
            "REMOTE_INPUT_PORT",
            "REMOTE_OUTPUT_PORT",
            "STATELESS_GROUP",
        ]

    entity_props = schemas.get("AffectedComponentEntity", {}).get("properties", {})
    ref_type = entity_props.get("referenceType", {})
    if ref_type and "enum" in ref_type:
        old_enum = ref_type["enum"]
        ref_type["enum"] = old_enum + [v for v in complete_enum if v not in old_enum]
        print(f"  AffectedComponentEntity.referenceType enum: {old_enum} -> {ref_type['enum']}")

    return spec


def main():
    if len(sys.argv) != 3:
        print("Usage: nifi_affected_component_reference_type.py <input.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        spec = json.load(f)

    spec = fix_affected_component_entity_reference_type(spec)

    with open(sys.argv[2], "w") as f:
        json.dump(spec, f, indent=2)


if __name__ == "__main__":
    main()
