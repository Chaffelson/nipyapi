#!/usr/bin/env python3
import json
import sys

"""
Augment a NiFi Registry OpenAPI JSON with proper securitySchemes and per-operation security.
- Adds components.securitySchemes: basicAuth (http basic), bearerAuth (http bearer JWT)
- Adds global security: bearerAuth
- Overrides:
  - POST /nifi-registry-api/access/token/login -> security: [ { basicAuth: [] } ]
  - POST /nifi-registry-api/access/token -> security: [] (try-all-providers)
Usage:
  python3 augment_registry_security.py <input_json> <output_json>
"""

LOGIN_PATH = "/access/token/login"
TRY_ALL_PATH = "/access/token"
BASE_PREFIX = "/nifi-registry-api"


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 augment_registry_security.py <input_json> <output_json>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r') as f:
        spec = json.load(f)

    # Ensure components exists
    components = spec.setdefault("components", {})
    # Inject securitySchemes
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes.setdefault("basicAuth", {"type": "http", "scheme": "basic"})
    security_schemes.setdefault("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})

    # Set global security to bearerAuth
    spec["security"] = [{"bearerAuth": []}]

    # Operation-level overrides
    paths = spec.get("paths", {})
    # Build full paths with prefix if needed
    def resolve(path_suffix):
        return BASE_PREFIX + path_suffix if (BASE_PREFIX + path_suffix) in paths else path_suffix

    login_key = resolve(LOGIN_PATH)
    try_all_key = resolve(TRY_ALL_PATH)

    if login_key in paths and "post" in paths[login_key]:
        paths[login_key]["post"]["security"] = [{"basicAuth": []}]

    if try_all_key in paths and "post" in paths[try_all_key]:
        paths[try_all_key]["post"]["security"] = []

    with open(outp, 'w') as f:
        json.dump(spec, f, indent=2)
    print("WROTE", outp)


if __name__ == "__main__":
    main()
