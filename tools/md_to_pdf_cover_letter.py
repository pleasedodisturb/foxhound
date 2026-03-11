#!/usr/bin/env python3
"""Convert markdown cover letters to clean PDF format.

Usage:
    python tools/md_to_pdf_cover_letter.py

Reads cover-letter.md from each application directory and generates cover-letter.pdf.
Edit the `dirs` list in main() to add new applications.

Requires: fpdf2 (pip install fpdf2)
Uses system Arial TTF fonts (macOS). Adapt font_dir for other platforms.
"""
import re
import sys
from pathlib import Path
from fpdf import FPDF


class CoverLetterPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        pass

    def footer(self):
        pass


def render_cover_letter(md_path: Path, pdf_path: Path):
    text = md_path.read_text(encoding="utf-8")
    lines = text.strip().split("\n")

    pdf = CoverLetterPDF()

    # Register Unicode fonts (Arial) — macOS paths; adapt for Linux/Windows
    font_dir = "/System/Library/Fonts/Supplemental"
    pdf.add_font("Arial", "", f"{font_dir}/Arial.ttf", uni=True)
    pdf.add_font("Arial", "B", f"{font_dir}/Arial Bold.ttf", uni=True)
    pdf.add_font("Arial", "I", f"{font_dir}/Arial Italic.ttf", uni=True)

    pdf.add_page()
    pdf.set_margins(25, 20, 25)
    pdf.set_y(20)

    name_font = ("Arial", "B", 18)
    contact_font = ("Arial", "", 9)
    date_font = ("Arial", "", 10)
    body_font = ("Arial", "", 10.5)
    bold_font = ("Arial", "B", 10.5)
    subject_font = ("Arial", "B", 11)

    i = 0
    in_body = False
    in_bullets = False

    while i < len(lines):
        line = lines[i].strip()

        # Skip horizontal rules
        if line == "---":
            if not in_body:
                pdf.set_draw_color(180, 180, 180)
                pdf.line(25, pdf.get_y() + 2, 185, pdf.get_y() + 2)
                pdf.ln(6)
            i += 1
            continue

        # Name (first line — adapt this check to your name)
        if i == 0 and not line.startswith("#"):
            pdf.set_font(*name_font)
            pdf.set_text_color(0, 50, 100)
            pdf.cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            i += 1
            continue

        # Contact line (detect by email domain or separator pattern)
        if ("@" in line or "·" in line) and not in_body and i < 5:
            pdf.set_font(*contact_font)
            pdf.set_text_color(80, 80, 80)
            clean = line.replace("·", "|")
            pdf.cell(0, 5, clean, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            i += 1
            continue

        # Date line
        if re.match(r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d", line):
            pdf.set_font(*date_font)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            i += 1
            continue

        # Subject line (bold, starts with **Re:)
        if line.startswith("**Re:"):
            in_body = True
            clean = line.replace("**", "")
            pdf.set_font(*subject_font)
            pdf.set_text_color(0, 50, 100)
            pdf.cell(0, 6, clean, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)
            i += 1
            continue

        # Empty line = paragraph break
        if line == "":
            if in_bullets:
                in_bullets = False
            pdf.ln(3)
            i += 1
            continue

        # Bullet points
        if line.startswith("- **"):
            in_bullets = True
            match = re.match(r"^- \*\*(.+?)\*\*\s*(.*)", line)
            if match:
                label = match.group(1)
                rest = match.group(2)
                pdf.set_text_color(30, 30, 30)
                rest = re.sub(r"\*\*(.+?)\*\*", r"\1", rest)

                indent = 30
                bullet_str = "\u2022  "

                pdf.set_font(*bold_font)
                bullet_w = pdf.get_string_width(bullet_str)
                label_w = pdf.get_string_width(label + " ")

                page_w = pdf.w - pdf.r_margin - indent
                first_line_remaining = page_w - bullet_w - label_w

                if rest and first_line_remaining < 40:
                    pdf.set_x(indent)
                    pdf.set_font(*bold_font)
                    pdf.cell(bullet_w, 5.5, bullet_str)
                    pdf.cell(label_w, 5.5, label)
                    pdf.ln(5.5)
                    pdf.set_font(*body_font)
                    pdf.set_x(indent + bullet_w)
                    pdf.multi_cell(page_w - bullet_w, 5.5, rest, new_x="LMARGIN", new_y="NEXT")
                elif rest:
                    pdf.set_x(indent)
                    pdf.set_font(*bold_font)
                    pdf.cell(bullet_w, 5.5, bullet_str)
                    pdf.cell(label_w, 5.5, label)

                    pdf.set_font(*body_font)
                    words = rest.split()
                    first_line_words = []
                    overflow_words = []
                    running_w = 0
                    filled = False
                    for w in words:
                        ww = pdf.get_string_width(w + " ")
                        if not filled and running_w + ww <= first_line_remaining:
                            first_line_words.append(w)
                            running_w += ww
                        else:
                            filled = True
                            overflow_words.append(w)

                    if first_line_words:
                        pdf.cell(0, 5.5, " ".join(first_line_words), new_x="LMARGIN", new_y="NEXT")
                    else:
                        pdf.ln(5.5)

                    if overflow_words:
                        pdf.set_x(indent + bullet_w)
                        pdf.multi_cell(page_w - bullet_w, 5.5, " ".join(overflow_words), new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.set_x(indent)
                    pdf.set_font(*bold_font)
                    pdf.cell(bullet_w, 5.5, bullet_str)
                    pdf.cell(0, 5.5, label, new_x="LMARGIN", new_y="NEXT")

                pdf.ln(1)
            i += 1
            continue

        # Regular body text
        in_body = True
        pdf.set_font(*body_font)
        pdf.set_text_color(30, 30, 30)

        clean = line
        clean = re.sub(r"\*\*(.+?)\*\*", r"\1", clean)
        clean = re.sub(r"\*(.+?)\*", r"\1", clean)

        pdf.multi_cell(0, 5.5, clean, new_x="LMARGIN", new_y="NEXT")
        i += 1

    pdf.output(str(pdf_path))
    print(f"  Created: {pdf_path}")


def main():
    # Update this path to your project root
    base = Path(__file__).resolve().parent.parent / "cv" / "applications"

    # Add your application directory names here
    dirs = [
        # "example-company-role-title",
    ]

    if not dirs:
        print("No application directories configured.")
        print("Edit the `dirs` list in this script to add your applications.")
        print(f"Application directories should be in: {base}")
        return

    for d in dirs:
        md_path = base / d / "cover-letter.md"
        pdf_path = base / d / "cover-letter.pdf"
        if md_path.exists():
            print(f"Converting {d}...")
            render_cover_letter(md_path, pdf_path)
        else:
            print(f"  SKIP: {md_path} not found")


if __name__ == "__main__":
    main()
