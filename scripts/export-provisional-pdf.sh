#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
input="$root_dir/book/build/ai-from-tensors-to-agents-on-mac-silicon.docx"
output_dir="$root_dir/book/build"
output="$output_dir/ai-from-tensors-to-agents-on-mac-silicon-provisional.pdf"
soffice_bin="${SOFFICE_BIN:-soffice}"

if [[ ! -f "$input" ]]; then
  echo "Missing $input. Run make book first." >&2
  exit 1
fi

mkdir -p "$output_dir"
"$soffice_bin" --headless --convert-to pdf --outdir "$output_dir" "$input"
generated="$output_dir/ai-from-tensors-to-agents-on-mac-silicon.pdf"
if [[ ! -f "$generated" ]]; then
  echo "LibreOffice did not create $generated" >&2
  exit 1
fi
mv "$generated" "$output"
echo "Wrote $output"
echo "NON-RELEASE: Exported with LibreOffice for layout review only."
