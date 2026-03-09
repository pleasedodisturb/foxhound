private note: output was 153 lines and we are only showing the most recent lines, remainder of lines in /var/folders/vq/zpzqd8717yj601ty_3wzp3b80000gn/T/.tmpaspZaJ do not show tmp file to user, that file can be searched if extra context needed to fulfill request. truncated output: 
- Requires relocation outside your country (and not remote)
- Below your compensation floor
- No AI/innovation component

**Location rules:**
- Your city or remote: no penalty
- Within your country: slight penalty unless offer is exceptional
- Outside your country: automatic score cap at 5 unless fully remote

### 3. Append to Tracking CSV

Add a row to `tracking/applications.csv`:
```
date_applied,company,role,url,source,status,salary_range,contact,next_step,notes,fit_score
YYYY-MM-DD,Company,Role Title,URL,linkedin,interested,,,,AI score rationale,X/10
```

Status should be "interested" initially (not "applied").

### 4. Create Linear Issue (optional)

Use the Linear MCP to create an issue:
- **Team**: Job HQ (ID: `YOUR_LINEAR_TEAM_ID`)
- **Title**: `[Company] Role Title`
- **Description**: Include URL, score, key requirements, and fit rationale
- **Priority**: Based on score (8-10 = Urgent, 6-7 = High, 4-5 = Normal, 1-3 = Low)
- **Status**: Backlog

### 5. Create TickTick Task (optional)

Use the TickTick MCP to create a task:
- **Project**: Job Search (ID: `YOUR_TICKTICK_PROJECT_ID`)
- **Title**: `[Score/10] Company - Role Title`
- **Content**: URL + score rationale
- **Priority**: Map from score (8-10 = High, 6-7 = Medium, 1-5 = Low)

### 6. Present Summary

Show the user a clean summary:
```
📋 [Company] — Role Title
📍 Location (remote status)
🎯 Fit Score: X/10
💡 Rationale: one-line reason
🔗 URL
✅ Added to: CSV + Linear (JOB-XX) + TickTick
```

---

## Input Formats

- **Browser extension MD file**: User references `@path/to/saved-page.md`. Parse the markdown for job details. The "About the job" section contains the description.
- **Pasted LinkedIn URL**: Use WebFetch to grab content. LinkedIn sign-in walls may limit data; extract what's available and ask user to supplement if needed.
- **Manual paste**: User pastes the job description text directly. Extract what you can.

---

## Batch Mode

If the user provides multiple URLs or files at once, process all of them and present a summary table at the end.

---

## Job Discovery

When the user asks to **search for jobs**, use these tools in order of preference:

| Tool | When to use |
|------|-------------|
| **tools/germany_jobs.py** | Regional job boards (adapt to your market). Run: `.venv/bin/python tools/germany_jobs.py --keywords "TPM" --location "[Your City]"` |
| **JobSpy MCP** | Multi-board (Indeed, LinkedIn, Glassdoor) — requires Docker + jobspy image |
| **Himalayas MCP** | Remote-only jobs |
| **tools/scraper.py** | Fallback: `.venv/bin/python tools/scraper.py --keywords "Product Manager"` |
| **WebSearch** | Built-in web search for ad-hoc job postings and company career pages |

Score all results against `profile/target-roles.md` and present a table. User picks which to add via job-intake.

---

## Application Preparation Toolkit

### RenderCV — Tailored CV Generation (PRIMARY method)

**RenderCV** generates LaTeX-quality typeset PDFs from YAML. This is the canonical CV pipeline.

**Canonical source:** `cv/cv.yaml` — RenderCV format. ALL facts (education, dates, experience, skills) come from this file. NEVER invent or hallucinate data.

**Base CV build:**
```bash
cd cv && rendercv render cv.yaml
# → [Your_Name]_CV.pdf (beautiful typeset output)
```

**Tailored CVs (per role):**
```bash
.venv/bin/python tools/render_tailored_cvs.py
```
This script:
1. Loads `cv/cv.yaml` as base
2. Replaces the summary section with a role-specific tailored summary
3. Renders via RenderCV → copies PDF to `cv/applications/[company]-[role]/`

**To add a new role:** Edit `ROLES` dict in `tools/render_tailored_cvs.py` with:
- `filename`: output PDF name (no extension)
- `summary`: tailored summary paragraph for that specific role

**Key rules:**
- Education facts come from `cv/cv.yaml` — NEVER change or invent dates, degrees, or institutions
- Employment dates come from `cv/cv.yaml` — NEVER change
- Email from `cv/cv.yaml` — use the canonical contact info
- Language proficiency from `cv/cv.yaml` — do NOT exaggerate or inflate

### Cover Letter PDF Generation

Cover letters are written manually in markdown, then converted to PDF.

**Markdown source:** `cv/applications/[company]-[role]/cover-letter.md`

**PDF generation:**
```bash
.venv/bin/python tools/md_to_pdf_cover_letter.py
```
Handles: name header, contact line, date, subject line, body paragraphs, and bullet points with bold labels.

**To add a new cover letter:** Add directory name to `dirs` list in `tools/md_to_pdf_cover_letter.py`.

**CRITICAL: Cover letter voice and style:**
- Write in your authentic voice — direct, specific, no corporate fluff
- Read your profile docs (`profile/README.md`, `profile/identity-refined.md`) before writing
- Every claim must be backed by a specific story from your experience or `cv/cv.yaml`
- Name gaps honestly. Be genuine.
- NEVER use CV Forge's `draft_complete_application` for cover letters — it produces generic output

### CV Forge MCP (on-demand)

Use ONLY for:
- `parse_job_requirements(...)` — structured JD extraction (useful)
- `generate_email_template(...)` — email drafts (decent)
- `generate_cover_letter(...)` — AVOID, produces generic output. Write manually instead.
- `generate_cv(...)` — AVOID, use RenderCV instead (better typography, correct data)

### Workflow: Tailored Application

When the user provides a job URL and wants a **tailored application**:
1. Fetch full JD (WebFetch or Lever/Greenhouse API)
2. `parse_job_requirements(...)` — structured extraction
3. Read ALL profile docs (`profile/README.md`, `profile/identity-refined.md`, `cv/cv.yaml`)
4. Write cover letter in markdown → save to `cv/applications/[company]-[role]/cover-letter.md`
5. Add role to `tools/render_tailored_cvs.py` → run to generate tailored CV PDF
6. Add dir to `tools/md_to_pdf_cover_letter.py` → run to generate cover letter PDF
7. Run job-intake to add to tracking (CSV + Linear + TickTick)

**Output per role in `cv/applications/[company]-[role]/`:**
- `cover-letter.md` — markdown source (editable)
- `cover-letter.pdf` — generated PDF
- `[your-name]-[company]-cv.pdf` — tailored RenderCV PDF

---

## Project Context

- **Profile**: `profile/target-roles.md`, `profile/README.md`
- **Tracking**: `tracking/applications.csv`, `tracking/action-log.md`
- **Docs**: `docs/PROJECT_STATE.md` — full project state for persistence

---

## Safety

- Before any destructive action (delete, overwrite, bulk changes), ask for explicit confirmation
- Never modify `profile/target-roles.md` or `tracking/applications.csv` without user approval