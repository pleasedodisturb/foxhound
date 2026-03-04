# Job Search HQ — Agent Instructions

**Shared by Cursor and Goose.** Workflow logic below is agent-agnostic.

Primary agent: **Goose** (CLI or Desktop). Cursor uses this file when running job intake in chat.

---

## Top of Mind (always remember)

- **Linear team ID:** `YOUR_LINEAR_TEAM_ID` ← replace with yours (optional integration)
- **TickTick project ID:** `YOUR_TICKTICK_PROJECT_ID` ← replace with yours (optional integration)
- Score roles against `profile/target-roles.md` before adding
- [Your city] or remote: no penalty; outside [your country]: cap score at 5
- Never delete or overwrite `tracking/applications.csv` without explicit user confirmation

---

## Job Intake Workflow

When the user shares a job posting (URL, saved markdown file from browser extension, or manual paste), follow this workflow:

### 1. Extract Structured Data

Parse the posting and extract:
- **Company**: name
- **Role**: full title
- **Location**: city/country + remote status
- **URL**: original posting link
- **Source**: linkedin / indeed / company site / etc.
- **Salary range**: if mentioned
- **Key requirements**: top 5 bullet points
- **Description summary**: 2-3 sentences

### 2. Score Against Profile

Score the role 1-10 against `profile/target-roles.md` and `profile/README.md`:

**High score factors (7-10):**
- AI/ML focus or genuine AI integration
- Remote-friendly or in your target city
- High autonomy, strategic thinking valued
- Matches your Tier 1 or Tier 2 companies
- Meets your compensation range

**Medium score factors (4-6):**
- Interesting company but role is process-heavy
- Requires some relocation within your country
- Bridge role (stepping stone, not dream)

**Low score factors (1-3):**
- Heavy PMBOK/PMO bureaucracy language
- Requires specific domain experience you lack
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
| **tools/germany_jobs.py** | Germany/regional roles; no Docker needed. Run: `python tools/germany_jobs.py --keywords "TPM" --location "Frankfurt"` |
| **JobSpy MCP** | Multi-board (Indeed, LinkedIn, Glassdoor) |
| **Brave Search** | Ad-hoc web search for job postings and company career pages |
| **tools/scraper.py** | Fallback: `python tools/scraper.py --keywords "Product Manager"` |

Score all results against `profile/target-roles.md` and present a table. User picks which to add via job-intake.

---

## Resume Tailoring

When the user provides a job URL and wants a **tailored application**:
1. Use **CV Forge MCP** to parse job requirements and generate tailored CV + cover letter
2. Output to PDF/HTML/MD as requested
3. Then run job-intake to add to tracking

---

## Project Context

- **Profile**: `profile/target-roles.md`, `profile/README.md`
- **Tracking**: `tracking/applications.csv`, `tracking/action-log.md`
- **Docs**: `docs/PROJECT_STATE.md` — full project state for persistence

---

## Safety

- Before any destructive action (delete, overwrite, bulk changes), ask for explicit confirmation
- Never modify `profile/target-roles.md` or `tracking/applications.csv` without user approval
