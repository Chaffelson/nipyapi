#!/usr/bin/env bash
set -euo pipefail

# Resolve directories regardless of invocation cwd
script_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"

# Instructions
# - Requires Java and either wget or curl
# - Generates client from OpenAPI and syncs apis/models/core client files into nipyapi

# Params
export wv_client_name=${wv_client_name:-all} # one of: nifi|registry|all
export wv_spec_variant=${wv_spec_variant:-augmented} # one of: augmented|base

# Codegen/tooling cache and working directory (repo-local by default)
export wv_codegen_version=${wv_codegen_version:-3.0.68}
export wv_codegen_filename=${wv_codegen_filename:-swagger-codegen-cli-${wv_codegen_version}.jar}
export wv_cache_dir=${wv_cache_dir:-"${script_dir}/_cache"}
export wv_tmp_dir=${wv_tmp_dir:-"${script_dir}/_tmp"}
export wv_client_dir="${wv_tmp_dir}/${wv_client_name}"
export wv_mustache_dir="${script_dir}/swagger_templates"
export wv_api_def_dir="${script_dir}/api_defs"

export wv_codegen_url="https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/${wv_codegen_version}/${wv_codegen_filename}"

# Preflight checks
command -v java >/dev/null 2>&1 || { echo "ERROR: Java not found on PATH" >&2; exit 1; }
[ -d "${wv_mustache_dir}" ] || { echo "ERROR: mustache template dir not found: ${wv_mustache_dir}" >&2; exit 1; }
[ -d "${wv_api_def_dir}" ] || { echo "ERROR: api_defs dir not found: ${wv_api_def_dir}" >&2; exit 1; }

mkdir -p "${wv_cache_dir}" "${wv_tmp_dir}"

# Download codegen jar if missing
if [ ! -f "${wv_cache_dir}/${wv_codegen_filename}" ]; then
  echo "Downloading ${wv_codegen_filename} to ${wv_cache_dir}"
  if command -v wget >/dev/null 2>&1; then
    wget -q --show-progress -O "${wv_cache_dir}/${wv_codegen_filename}" "${wv_codegen_url}"
  else
    curl -fL --retry 3 --retry-delay 2 -o "${wv_cache_dir}/${wv_codegen_filename}" "${wv_codegen_url}"
  fi
fi


generate_and_sync() {
  local client_name="$1"
  local client_dir="${wv_tmp_dir}/${client_name}"
  local swagger_def
  if [ "${wv_spec_variant}" = "augmented" ]; then
    # Prefer augmented specs (e.g., nifi-<ver>.augmented.json)
    swagger_def=$(ls "${wv_api_def_dir}" | grep "^${client_name}-" | grep -E 'augmented\\.json$' | sort -V | tail -1 || true)
  fi
  if [ -z "${swagger_def:-}" ]; then
    # Fall back to base spec (exclude augmented files)
    swagger_def=$(ls "${wv_api_def_dir}" | grep "^${client_name}-" | grep -v 'augmented\\.json$' | sort -V | tail -1 || true)
  fi
  if [ -z "${swagger_def}" ]; then
    echo "ERROR: No API definition found for ${client_name} in ${wv_api_def_dir}" >&2
    echo "Hint: run 'make fetch-openapi' to fetch and augment specs from running containers." >&2
    exit 1
  fi
  # Create per-client config (python3-only, suppress timestamps)
  mkdir -p "${wv_tmp_dir}"
  cat > "${wv_tmp_dir}/${client_name}.conf.json" <<EOF
{
  "packageName": "${client_name}",
  "projectName": "nipyapi-${client_name}",
  "pythonLegacySupport": false,
  "hideGenerationTimestamp": true
}
EOF
  echo "Generating client for ${client_name} from ${swagger_def} (variant=${wv_spec_variant})"
  mkdir -p "${wv_client_dir}"
  java -jar "${wv_cache_dir}/${wv_codegen_filename}" generate \
      -l python \
      -c "${wv_tmp_dir}/${client_name}.conf.json" \
      --api-package apis \
      --model-package models \
      -t "${wv_mustache_dir}" \
      -i "${wv_api_def_dir}/${swagger_def}" \
      -Dmodels,apis,supportingFiles,apiDocs=false,modelDocs=false,apiTests=false,modelTests=false \
      -o "${client_dir}"

  # Verify generation produced expected structure
  if [ ! -d "${client_dir}/${client_name}/apis" ] || [ ! -d "${client_dir}/${client_name}/models" ]; then
    echo "ERROR: Generated output missing expected directories under ${client_dir}/${client_name}" >&2
    exit 1
  fi

  echo "Syncing generated client into ${repo_root}/nipyapi/${client_name}"
  target_pkg="${repo_root}/nipyapi/${client_name}"
  mkdir -p "${target_pkg}/apis" "${target_pkg}/models"
  rsync -a --delete "${client_dir}/${client_name}/apis/" "${target_pkg}/apis/"
  rsync -a --delete "${client_dir}/${client_name}/models/" "${target_pkg}/models/"
  for f in api_client.py rest.py configuration.py __init__.py; do
    if [ -f "${client_dir}/${client_name}/${f}" ]; then
      cp "${client_dir}/${client_name}/${f}" "${target_pkg}/${f}"
    fi
  done
}

if [ "${wv_client_name}" = "all" ]; then
  for c in nifi registry; do
    generate_and_sync "$c"
  done
else
  generate_and_sync "${wv_client_name}"
fi

echo Done.
