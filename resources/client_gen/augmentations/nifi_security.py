#!/usr/bin/env python3
import json, sys

LOGIN_PATH = "/access/token"
BASE_PREFIX = "/nifi-api"

def main():
    if len(sys.argv) != 3:
        print("Usage: nifi_security.py <input_json> <output_json>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r') as f:
        spec = json.load(f)
    components = spec.setdefault("components", {})
    schemes = components.setdefault("securitySchemes", {})
    schemes.setdefault("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})
    spec["security"] = [{"bearerAuth": []}]
    paths = spec.get("paths", {})
    def resolve(path_suffix):
        return BASE_PREFIX + path_suffix if (BASE_PREFIX + path_suffix) in paths else path_suffix
    login_key = resolve(LOGIN_PATH)
    if login_key in paths and "post" in paths[login_key]:
        paths[login_key]["post"]["security"] = []
    with open(outp, 'w') as f:
        json.dump(spec, f, indent=2)

if __name__ == '__main__':
    main()

