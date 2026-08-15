#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template="$root_dir/book/templates/lulu-us-trade-interior-template.dotx"
output_dir="$root_dir/book/build"

if [[ ! -f "$template" ]]; then
  echo "Missing $template. See book/templates/README.md." >&2
  exit 1
fi

mkdir -p "$output_dir"
chapter_files=("$root_dir"/book/chapters/*.md)
pandoc "${chapter_files[@]}" --metadata-file="$root_dir/book/manuscript.yaml" \
  --resource-path="$root_dir/book" --reference-doc="$template" \
  --citeproc --output="$output_dir/from-tensors-to-agents.docx"
echo "Wrote $output_dir/from-tensors-to-agents.docx"
