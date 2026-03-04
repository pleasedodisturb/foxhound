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