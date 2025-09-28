#!/usr/bin/env python3
import json, sys

LOGIN_PATH = "/access/token/login"
TRY_ALL_PATH = "/access/token"
BASE_PREFIX = "/nifi-registry-api"

def main():
    if len(sys.argv) != 3:
        print("Usage: registry_security.py <input_json> <output_json>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r') as f:
        spec = json.load(f)
    components = spec.setdefault("components", {})
    schemes = components.setdefault("securitySchemes", {})
    schemes.setdefault("basicAuth", {"type": "http", "scheme": "basic"})
    schemes.setdefault("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})
    spec["security"] = [{"bearerAuth": []}]
    paths = spec.get("paths", {})
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

if __name__ == '__main__':
    main()

