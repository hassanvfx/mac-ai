#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template="$root_dir/book/templates/lulu-us-trade-interior-template.dotx"
output_dir="$root_dir/book/build"
prepared_dir="$(mktemp -d)"

cleanup() {
  rm -rf "$prepared_dir"
}
trap cleanup EXIT

if [[ ! -f "$template" ]]; then
  echo "Missing $template. See book/templates/README.md." >&2
  exit 1
fi

mkdir -p "$output_dir"
mkdir -p "$prepared_dir/chapters"
mkdir -p "$prepared_dir/appendices"
cp -R "$root_dir/book/assets" "$prepared_dir/assets"
chapter_files=()
for source_file in "$root_dir"/book/chapters/*.md "$root_dir"/book/appendices/*.md; do
  section_dir="chapters"
  if [[ "$source_file" == *"/appendices/"* ]]; then
    section_dir="appendices"
  fi
  prepared_file="$prepared_dir/$section_dir/$(basename "$source_file")"
  # Docusaurus needs YAML front matter for sidebar metadata. Pandoc treats the
  # same blocks as document metadata and lets a chapter title overwrite the
  # manuscript title, so remove only a leading front-matter block in this
  # temporary print-only copy.
  awk '
    NR == 1 && $0 == "---" { in_front_matter = 1; next }
    in_front_matter && $0 == "---" { in_front_matter = 0; next }
    # The temporary chapter copies live one directory deeper than the original
    # chapters, so make canonical book assets relative to the temporary root.
    !in_front_matter { gsub(/]\(\.\.\/assets\//, "](assets/"); print }
  ' "$source_file" > "$prepared_file"
  chapter_files+=("$prepared_file")
done
pandoc "${chapter_files[@]}" --metadata-file="$root_dir/book/manuscript.yaml" \
  --resource-path="$prepared_dir:$root_dir/book" --reference-doc="$template" \
  --citeproc --output="$output_dir/from-tensors-to-agents.docx"
echo "Wrote $output_dir/from-tensors-to-agents.docx"
