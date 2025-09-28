#!/usr/bin/env bash
set -euo pipefail

# Fetch NiFi OpenAPI spec from a running container by copying from filesystem.
# Usage: NIFI_VERSION=2.5.0 ./fetch_nifi_openapi.sh [container_name]

script_dir="$(cd "$(dirname "$0")" && pwd)"
api_defs_dir="${script_dir}/api_defs"
nifi_version="${NIFI_VERSION:-2.5.0}"
container_name="${1:-${NIFI_CONTAINER:-nifi-single}}"

if ! docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
  echo "ERROR: Container '${container_name}' not running. Start a compose profile first." >&2
  exit 1
fi

echo "Searching for NiFi OpenAPI/Swagger spec inside container '${container_name}'"
spec_path=$(docker exec "${container_name}" sh -lc "set -e; find /opt -type f \
  \( -iname '*openapi*.json' -o -iname '*swagger*.json' \) 2>/dev/null | head -n 1") || true

if [ -z "${spec_path}" ]; then
  echo "ERROR: Could not locate an OpenAPI/Swagger JSON inside ${container_name}" >&2
  exit 1
fi

mkdir -p "${api_defs_dir}"
out_file="${api_defs_dir}/nifi-${nifi_version}.json"
tmp_file="${api_defs_dir}/.nifi-openapi-tmp.json"

echo "Copying '${spec_path}' to '${out_file}'"
docker cp "${container_name}:${spec_path}" "${tmp_file}"

# Ensure JSON extension and pretty minimal check
mv "${tmp_file}" "${out_file}"
echo "WROTE ${out_file}"
exit 0
#!/usr/bin/env bash
set -euo pipefail

# Attempt to obtain NiFi OpenAPI/Swagger from a running container (compose) or a disposable one.
# Writes to resources/client_gen/api_defs/nifi-<version>.yaml or .json depending on source.

script_dir="$(cd "$(dirname "$0")" && pwd)"
api_defs_dir="${script_dir}/api_defs"
mkdir -p "${api_defs_dir}"

container_name="${NIFI_CONTAINER:-nifi}"
base_url_env="${NIFI_API_ENDPOINT:-}"

# Require a running container (compose) unless NIFI_API_ENDPOINT is provided
if [[ -z "${base_url_env}" ]]; then
  if ! docker ps --format '{{.Names}}' | grep -qx "${container_name}"; then
    echo "Container '${container_name}' is not running. Start it with:"
    echo "  docker compose -f resources/docker/latest/docker-compose.yml up -d"
    exit 1
  fi
fi

# Determine mapped port for 8443
if [[ -n "${base_url_env}" ]]; then
  base_url="${base_url_env}"
else
  host_port="$(docker inspect -f '{{ (index (index .NetworkSettings.Ports "8443/tcp") 0).HostPort }}' "${container_name}" 2>/dev/null || true)"
  base_url=""
  if [[ -n "${host_port}" && "${host_port}" != "<no value>" ]]; then
    base_url="https://localhost:${host_port}"
    echo "Resolved mapped host port for 8443/tcp -> ${host_port}"
  else
    # Fall back to container IP if compose-style networking (not ideal for localhost access)
    ip="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${container_name}")"
    base_url="https://${ip}:8443"
    echo "Using container IP fallback ${ip}:8443"
  fi
fi

echo "Using base URL: ${base_url}"

# Wait for readiness
echo -n "Waiting for NiFi to be ready"
for i in {1..300}; do
  code=$(curl -k -s -o /dev/null -w "%{http_code}" "${base_url}/nifi-api/flow/about" || true)
  if [[ "$code" == "200" || "$code" == "401" ]]; then
    echo " - ready (${code})"
    break
  fi
  echo -n "."
  sleep 2
  if [[ $i -eq 300 ]]; then
    echo "\nNiFi did not become ready in time" >&2
    exit 1
  fi
done

# Try to discover version from about; if empty, will fill later based on file path or spec info
version=""
if command -v jq >/dev/null 2>&1; then
  version=$(curl -k -sS "${base_url}/nifi-api/flow/about" 2>/dev/null | jq -r '(.about.version // .about.buildTag // empty)' 2>/dev/null || true)
fi

echo "Detected NiFi version: ${version}"

echo "Searching container for swagger/openapi artifacts..."
container_spec_path=$(docker exec "${container_name}" bash -lc "set -e; \
  find /opt/nifi -type f \
    \( -name openapi.yaml -o -name openapi.json -o -name swagger.yaml -o -name swagger.json \) 2>/dev/null \
    | sort | head -n 1")

if [[ -z "${container_spec_path}" ]]; then
  echo "No swagger/openapi file found in NiFi container. NiFi typically does not publish the spec at runtime." >&2
  echo "Fallback options:" >&2
  echo " - Build from source using the swagger maven plugin at the appropriate module and copy the output." >&2
  echo " - Provide a prebuilt spec file manually under ${api_defs_dir}/nifi-${version}.json (or .yaml)." >&2
  exit 2
fi

ext="${container_spec_path##*.}"
# If version is still empty, try to parse from the path (e.g., nifi-web-api-2.5.0.war)
if [[ -z "${version}" ]]; then
  parsed="$(basename "${container_spec_path}" | sed -n 's/.*-\([0-9][0-9.]*\)\.war.*/\1/p')"
  if [[ -n "${parsed}" ]]; then
    version="${parsed}"
  else
    # Last fallback: read .info.version if JSON
    if [[ "${ext}" == "json" ]] && command -v jq >/dev/null 2>&1; then
      tmpfile="${api_defs_dir}/nifi-tmp.json"
      docker cp "${container_name}:${container_spec_path}" "${tmpfile}"
      v2=$(jq -r '(.info.version // empty)' "${tmpfile}" || true)
      if [[ -n "${v2}" ]]; then version="${v2}"; fi
      rm -f "${tmpfile}"
    fi
  fi
fi

outfile="${api_defs_dir}/nifi-${version}.${ext}"
echo "Copying ${container_spec_path} -> ${outfile}"
docker cp "${container_name}:${container_spec_path}" "${outfile}"
echo "Wrote ${outfile}"

echo "Done."

