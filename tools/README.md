# Tools

Python scripts for job discovery, scoring, and application generation. All runnable standalone — no AI agent required.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Scripts

### germany_jobs.py

Searches German job boards: Arbeitsagentur (federal) and Arbeitnow (English-language). Adapt for your country's boards.

```bash
.venv/bin/python tools/germany_jobs.py --preset ai --location Berlin
.venv/bin/python tools/germany_jobs.py --preset builder
.venv/bin/python tools/germany_jobs.py --keywords "Product Manager AI" --output results.json
```

### job_scorer.py

Batch scores a CSV of scraped jobs using GPT-4o-mini. Reads scoring criteria from an internal prompt — customize the `PROFILE_CRITERIA` variable in the script to match your `profile/target-roles.md`. Adds `fit_score`, `fit_reasoning`, `estimated_salary`, `effort_flag`, `prep_level`, and `prep_notes` columns.

```bash
export OPENAI_API_KEY=your_key
.venv/bin/python tools/job_scorer.py tracking/scraped_jobs.csv
```

Output: `tracking/scraped_jobs_scored.csv`

### scraper.py

Multi-board job scraper via [python-jobspy](https://github.com/cullenwatson/JobSpy). Searches Indeed, LinkedIn, Glassdoor.

```bash
.venv/bin/python tools/scraper.py
```

### render_tailored_cvs.py

Generates per-role tailored CVs from `cv/cv.yaml` via RenderCV. Edit the `ROLES` dict in the script to add role-specific summaries.

```bash
.venv/bin/python tools/render_tailored_cvs.py
```

### md_to_pdf_cover_letter.py

Converts markdown cover letters to formatted PDFs via fpdf2. Reads from `cv/applications/[company-role]/cover-letter.md`.

```bash
.venv/bin/python tools/md_to_pdf_cover_letter.py
```

### weekly-scan.sh

Shell wrapper for running a weekly discovery scan. Can be scheduled via cron or launchd.
