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
front_matter="$prepared_dir/front-matter.md"
cp "$root_dir/book/front-matter.md" "$front_matter"
chapter_files=("$front_matter")
for source_file in "$root_dir"/book/chapters/*.md "$root_dir"/book/appendices/*.md; do
  section_dir="chapters"
  if [[ "$source_file" == *"/appendices/"* ]]; then
    section_dir="appendices"
  fi
  prepared_file="$prepared_dir/$section_dir/$(basename "$source_file")"
  # Keep canonical Markdown free of generated publishing furniture. This
  # temporary print copy strips Docusaurus front matter and appends the QR lab
  # panel from the single reader-bridge manifest.
  python3 "$root_dir/scripts/prepare_print_chapter.py" "$source_file" "$prepared_file"
  chapter_files+=("$prepared_file")
done
pandoc "${chapter_files[@]}" --metadata-file="$root_dir/book/manuscript.yaml" \
  --resource-path="$prepared_dir:$root_dir/book" --reference-doc="$template" \
  --standalone --lua-filter="$root_dir/scripts/book_layout.lua" --citeproc \
  --output="$output_dir/ai-from-tensors-to-agents-on-mac-silicon.docx"
python3 "$root_dir/scripts/normalize_docx_trim.py" \
  "$output_dir/ai-from-tensors-to-agents-on-mac-silicon.docx"
echo "Wrote $output_dir/ai-from-tensors-to-agents-on-mac-silicon.docx"
