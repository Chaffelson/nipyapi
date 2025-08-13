#!/usr/bin/env python3
"""
Normalize OpenAPI enums in JSON specs:
- Split single-item comma-joined enums into discrete values
- Deduplicate enum arrays while preserving order

Usage:
  normalize_openapi_enums.py <input.json> <output.json>

Notes:
- JSON only. Does not process YAML.
- Writes to the provided output path; does not modify the input file.
"""

from __future__ import annotations

import json
import sys
from typing import Any, List


def split_comma_joined_enum(enum_list: List[Any]) -> List[Any]:
    """If enum_list is a single string with commas, split into multiple strings; otherwise return as-is."""
    if len(enum_list) == 1 and isinstance(enum_list[0], str) and "," in enum_list[0]:
        return [part.strip() for part in enum_list[0].split(",") if part.strip()]
    return enum_list


def deduplicate_preserve_order(seq: List[Any]) -> List[Any]:
    seen = set()
    result: List[Any] = []
    for item in seq:
        key = json.dumps(item, sort_keys=True) if not isinstance(item, (str, int, float, bool, type(None))) else item
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def normalize_enums(node: Any) -> Any:
    if isinstance(node, dict):
        # Normalize enums if present
        if "enum" in node and isinstance(node["enum"], list):
            enum_vals = node["enum"]
            enum_vals = split_comma_joined_enum(enum_vals)
            enum_vals = deduplicate_preserve_order(enum_vals)
            node["enum"] = enum_vals
        # Recurse into values
        for k, v in list(node.items()):
            node[k] = normalize_enums(v)
        return node
    if isinstance(node, list):
        return [normalize_enums(item) for item in node]
    return node


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: normalize_openapi_enums.py <input.json> <output.json>", file=sys.stderr)
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    if not input_path.lower().endswith(".json"):
        print("Input must be a JSON file", file=sys.stderr)
        sys.exit(2)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = normalize_enums(data)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()


