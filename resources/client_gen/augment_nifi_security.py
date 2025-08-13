#!/usr/bin/env python3
import json
import sys

"""
Augment a NiFi OpenAPI JSON with proper bearer security and per-operation overrides.
- Adds components.securitySchemes: bearerAuth (http bearer JWT)
- Adds global security: bearerAuth
- Overrides:
  - POST /nifi-api/access/token -> security: [] (form-based login)
Usage:
  python3 augment_nifi_security.py <input_json> <output_json>
"""

LOGIN_PATH = "/access/token"
BASE_PREFIX = "/nifi-api"


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 augment_nifi_security.py <input_json> <output_json>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r') as f:
        spec = json.load(f)

    # Ensure components exists
    components = spec.setdefault("components", {})
    # Inject securitySchemes
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes.setdefault("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})

    # Set global security to bearerAuth
    spec["security"] = [{"bearerAuth": []}]

    # Operation-level override for form-based login
    paths = spec.get("paths", {})

    def resolve(path_suffix):
        return BASE_PREFIX + path_suffix if (BASE_PREFIX + path_suffix) in paths else path_suffix

    login_key = resolve(LOGIN_PATH)

    if login_key in paths and "post" in paths[login_key]:
        paths[login_key]["post"]["security"] = []

    with open(outp, 'w') as f:
        json.dump(spec, f, indent=2)
    print("WROTE", outp)


if __name__ == "__main__":
    main()
