#!/usr/bin/env bash
set -euo pipefail

# Fetch NiFi Registry OpenAPI spec from a running container by copying from filesystem,
# falling back to the HTTP endpoint if present.
# Usage: NIFI_VERSION=2.5.0 ./fetch_registry_openapi.sh [container_name]

script_dir="$(cd "$(dirname "$0")" && pwd)"
api_defs_dir="${script_dir}/api_defs"
reg_version="${NIFI_VERSION:-2.5.0}"
container_name="${1:-${REGISTRY_CONTAINER:-registry-single}}"

if ! docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
  echo "ERROR: Container '${container_name}' not running. Start a compose profile first." >&2
  exit 1
fi

mkdir -p "${api_defs_dir}"
out_file="${api_defs_dir}/registry-${reg_version}.json"
tmp_file="${api_defs_dir}/.registry-openapi-tmp.json"

# Try filesystem copy first
echo "Searching for Registry OpenAPI JSON inside '${container_name}'"
spec_path=$(docker exec "${container_name}" sh -lc "set -e; find /opt -type f \
  \( -iname '*openapi*.json' -o -iname '*swagger*.json' \) 2>/dev/null | head -n 1") || true
if [ -n "${spec_path}" ]; then
  echo "Copying '${spec_path}' to '${out_file}'"
  docker cp "${container_name}:${spec_path}" "${tmp_file}"
  mv "${tmp_file}" "${out_file}"
echo "WROTE ${out_file}"
exit 0
fi

# Fallback to HTTP(S) endpoint; prefer REGISTRY_API_ENDPOINT if provided
echo "Falling back to /nifi-registry-api/swagger.json"
base_url="${REGISTRY_API_ENDPOINT:-}"
try_urls=()
if [ -n "${base_url}" ]; then
  try_urls+=("${base_url}/swagger.json")
fi
# Common local defaults
try_urls+=(
  "https://localhost:18443/nifi-registry-api/swagger.json"
  "http://localhost:18080/nifi-registry-api/swagger.json"
)

set +e
rc=1
for u in "${try_urls[@]}"; do
  echo "  trying ${u}"
  curl -fsSk "${u}" -o "${tmp_file}"
  rc=$?
  [ $rc -eq 0 ] && { echo "  fetched ${u}"; break; }
done
set -e
if [ $rc -ne 0 ]; then
  echo "ERROR: Unable to fetch Registry OpenAPI via HTTP fallback" >&2
  exit 1
fi
mv "${tmp_file}" "${out_file}"
echo "WROTE ${out_file}"
#!/usr/bin/env bash
set -euo pipefail

# Fetch the NiFi Registry OpenAPI/Swagger from a running compose service 'registry'
# and store it under api_defs/registry-<version>.yaml or .json

script_dir="$(cd "$(dirname "$0")" && pwd)"
api_defs_dir="${script_dir}/api_defs"
mkdir -p "${api_defs_dir}"

container_name="${REGISTRY_CONTAINER:-registry}"
if ! docker ps --format '{{.Names}}' | grep -qx "${container_name}"; then
  echo "Container '${container_name}' is not running. Start it with:"
  echo "  docker compose -f resources/docker/latest/docker-compose.yml up -d"
  exit 1
fi

# Determine mapped host port for container's 18080/tcp
echo "Resolving mapped host port..."
host_port="$(docker inspect -f '{{ (index (index .NetworkSettings.Ports "18080/tcp") 0).HostPort }}' "${container_name}")"
if [[ -z "${host_port}" || "${host_port}" == "<no value>" ]]; then
  echo "Failed to resolve mapped host port for 18080/tcp" >&2
  exit 1
fi
base_url="http://localhost:${host_port}"
echo "Registry base URL: ${base_url}"

# Wait for service readiness (about endpoint)
echo -n "Waiting for NiFi Registry to become ready"
for i in {1..60}; do
  if curl -fsS "${base_url}/nifi-registry-api/about" >/dev/null 2>&1; then
    echo " - ready"
    break
  fi
  echo -n "."
  sleep 2
  if [[ $i -eq 60 ]]; then
    echo "\nRegistry did not become ready in time" >&2
    exit 1
  fi
done

version=""
if command -v jq >/dev/null 2>&1; then
  version=$(curl -fsS "${base_url}/nifi-registry-api/about" | jq -r '(.registryAboutVersion // .about.version // empty)') || true
fi
if [[ -z "${version}" ]]; then
  version="${image##*:}"
fi

# Try fetching via HTTP endpoints first
declare -a http_paths=(
  "/nifi-registry-api/openapi.json"
  "/nifi-registry-api/swagger.json"
  "/nifi-registry-api/api-docs"
)
spec_json=""
for p in "${http_paths[@]}"; do
  if spec_json=$(curl -fsS "${base_url}${p}" 2>/dev/null); then
    outfile="${api_defs_dir}/registry-${version}.json"
    echo "Fetched spec from ${p}; writing ${outfile}"
    printf '%s' "${spec_json}" > "${outfile}"
    echo "Done."
    exit 0
  fi
done

echo "HTTP spec endpoints not found; copying from container filesystem"

# Find openapi/swagger file inside the container (prefer JSON for consistency)
container_spec_path=$(docker exec "${container_name}" sh -lc '
  set -e;
  for name in swagger.json openapi.json swagger.yaml openapi.yaml; do
    res=$(find /opt/nifi-registry -type f -name "$name" 2>/dev/null | head -n 1)
    if [ -n "$res" ]; then echo "$res"; break; fi
  done
')

if [[ -z "${container_spec_path}" ]]; then
  echo "Unable to locate openapi/swagger file inside container" >&2
  exit 1
fi

ext="${container_spec_path##*.}"
# If YAML found but JSON is expected, convert when jq is available
dest="${api_defs_dir}/registry-${version}.json"
if [[ "${ext}" == "json" ]]; then
  echo "Copying ${container_spec_path} -> ${dest}"
  docker cp "${container_name}:${container_spec_path}" "${dest}"
else
  # Try convert YAML->JSON using yq if installed; otherwise copy YAML but name with .yaml
  if command -v yq >/dev/null 2>&1; then
    tmp_yaml="${api_defs_dir}/registry-${version}.yaml"
    echo "Copying ${container_spec_path} -> ${tmp_yaml} and converting to JSON"
    docker cp "${container_name}:${container_spec_path}" "${tmp_yaml}"
    yq -o=json "${tmp_yaml}" > "${dest}"
    rm -f "${tmp_yaml}"
  else
    dest_yaml="${api_defs_dir}/registry-${version}.yaml"
    echo "Copying ${container_spec_path} -> ${dest_yaml} (no yq available for conversion)"
    docker cp "${container_name}:${container_spec_path}" "${dest_yaml}"
    echo "Wrote ${dest_yaml}"
    echo "Done."
    exit 0
  fi
fi
echo "Wrote ${dest}"

echo "Done."

