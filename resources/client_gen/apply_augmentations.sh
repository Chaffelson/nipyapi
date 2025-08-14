#!/usr/bin/env bash
set -euo pipefail

# Apply all augmentation scripts for a given service to an OpenAPI JSON.
# Usage: ./apply_augmentations.sh <service:nifi|registry> <input_json> <output_json>
#
# Looks for Python scripts under resources/client_gen/augmentations matching:
#   common_*.py for all services
#   nifi_*.py for service=nifi
#   registry_*.py for service=registry
# Applies them in sorted filename order, chaining input->output.
#
# Each augmentation script must accept: <input_json> <output_json>

script_dir="$(cd "$(dirname "$0")" && pwd)"
aug_dir="${script_dir}/augmentations"

service="${1:-}"
in_json="${2:-}"
out_json="${3:-}"

if [ -z "${service}" ] || [ -z "${in_json}" ] || [ -z "${out_json}" ]; then
  echo "Usage: $0 <service:nifi|registry> <input_json> <output_json>" >&2
  exit 1
fi

if [ ! -f "${in_json}" ]; then
  echo "ERROR: input JSON not found: ${in_json}" >&2
  exit 1
fi

mkdir -p "${aug_dir}"

tmp_work="${out_json}.tmp.work"
cp "${in_json}" "${tmp_work}"

shopt -s nullglob
applied=0
# First apply any common augmentations (service-agnostic)
for aug in "${aug_dir}/common"_*.py; do
  next="${tmp_work}.next"
  echo "Applying augmentation: $(basename "$aug")"
  python "$aug" "${tmp_work}" "${next}"
  mv "${next}" "${tmp_work}"
  applied=$((applied+1))
done

# Then apply service-specific augmentations
for aug in "${aug_dir}/${service}"_*.py; do
  next="${tmp_work}.next"
  echo "Applying augmentation: $(basename "$aug")"
  python "$aug" "${tmp_work}" "${next}"
  mv "${next}" "${tmp_work}"
  applied=$((applied+1))
done
shopt -u nullglob

mv "${tmp_work}" "${out_json}"
echo "APPLIED ${applied} augmentation(s) -> ${out_json}"

