#!/usr/bin/env bash
# Build CV outputs from cv.yaml using RenderCV.
# Requires: rendercv (pip install rendercv)
# Optional: pandoc (for DOCX output)
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Building CV ==="

echo "[1/2] RenderCV → PDF + HTML"
rendercv render cv.yaml

# Optional: build a second language variant
# echo "[2/3] RenderCV → German PDF (Lebenslauf)"
# rendercv render cv_de.yaml

# Optional: generate DOCX via pandoc
# echo "[3/3] Pandoc → DOCX"
# pandoc cv.md -o Your_Name_CV.docx --reference-doc=reference.docx

echo ""
echo "Done! Check the output files in this directory."
