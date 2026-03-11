#!/usr/bin/env python3
"""Generate tailored CV PDFs from cv.yaml using RenderCV.

Creates a temporary YAML variant per role with a tailored summary,
renders it, and copies the PDF to the application folder.

Usage:
    python tools/render_tailored_cvs.py

Requires: rendercv (pip install rendercv), pyyaml

Edit the ROLES dict below to add your tailored applications.
"""
import copy
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent / "cv"
APP_DIR = BASE_DIR / "applications"
# Update this path to your rendercv binary location
RENDERCV = str(BASE_DIR.parent / ".venv" / "bin" / "rendercv")

# Tailored summaries per role — edit these for your applications
ROLES = {
    # "example-company-role-title": {
    #     "filename": "your-name-company-cv",
    #     "summary": (
    #         "Your tailored summary for this specific role. "
    #         "Highlight the experience and skills most relevant to the position. "
    #         "Keep it concise — 3-4 sentences max."
    #     ),
    # },
}


def load_base_yaml():
    """Load and parse the base cv.yaml."""
    with open(BASE_DIR / "cv.yaml") as f:
        return yaml.safe_load(f)


def render_variant(role_key: str, role_config: dict, base_data: dict):
    """Create a tailored YAML, render it, copy PDF to application folder."""
    variant = copy.deepcopy(base_data)

    # Replace summary
    variant["cv"]["sections"]["summary"] = [role_config["summary"]]

    # Write temp YAML
    temp_yaml = BASE_DIR / f"cv_tailored_{role_key}.yaml"
    with open(temp_yaml, "w") as f:
        yaml.dump(variant, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Render
    print(f"\n  Rendering {role_key}...")
    result = subprocess.run(
        [RENDERCV, "render", str(temp_yaml)],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return False

    # Copy PDF to application folder
    src_pdf = BASE_DIR / f"{role_config['filename']}.pdf"
    dst_dir = APP_DIR / role_key
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_pdf = dst_dir / f"{role_config['filename']}.pdf"

    if src_pdf.exists():
        shutil.copy2(src_pdf, dst_pdf)
        print(f"  ✓ {dst_pdf}")
        # Clean up temp files from base dir
        src_pdf.unlink()
        src_html = BASE_DIR / f"{role_config['filename']}.html"
        if src_html.exists():
            src_html.unlink()
    else:
        print(f"  ERROR: PDF not found at {src_pdf}")
        return False

    # Clean up temp YAML
    temp_yaml.unlink()

    return True


def main():
    if not ROLES:
        print("No roles configured.")
        print("Edit the ROLES dict in this script to add your tailored applications.")
        print(f"Base CV: {BASE_DIR / 'cv.yaml'}")
        print(f"Application output: {APP_DIR}")
        return

    print("Loading base cv.yaml...")
    base_data = load_base_yaml()

    successes = 0
    for role_key, role_config in ROLES.items():
        if render_variant(role_key, role_config, base_data):
            successes += 1

    print(f"\n{'='*50}")
    print(f"Done: {successes}/{len(ROLES)} CVs generated successfully")


if __name__ == "__main__":
    main()
