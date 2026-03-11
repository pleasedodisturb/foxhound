Process a job posting and add it to tracking.

## Input

$ARGUMENTS

The input is a job posting URL, a path to a saved markdown file, or pasted job description text.

## Instructions

Read `AGENT.md` for the full workflow, then execute these steps:

### Step 1 — Fetch and Extract

If the input is a URL: use WebFetch to retrieve the job posting content.
If the input is a file path: read the file.
If the input is pasted text: use it directly.

Extract structured data:
- **Company**: name
- **Role**: full title
- **Location**: city/country + remote status
- **URL**: original posting link
- **Source**: linkedin / indeed / company site / etc.
- **Salary range**: if mentioned, else empty
- **Key requirements**: top 5 bullet points
- **Description summary**: 2-3 sentences

### Step 2 — Score 1-10

Score against `profile/target-roles.md` and `profile/README.md`.

Apply ALL modifiers from `AGENT.md` scoring section:
- Base: does the role intent match your target profile? Start at 5.
- AI-native company or genuine AI product: +1
- Remote-friendly or in your target city: no penalty (otherwise -1 to -3)
- Builder signals in JD (shipping, pipelines, building, tools): +1
- Early-stage / founding team: +1
- Dream company (check profile/target-roles.md tier lists): floor at appropriate tier score
- PMBOK/process-heavy, no AI: -2
- Outside your country, not remote: cap at 5
- Below target salary floor: -1
- No title match but strong intent match: still score 7+ if everything else fits

Write a 1-sentence rationale.

### Step 3 — Append to CSV

Append ONE row to `tracking/applications.csv`. Format:
```
date_applied,company,role,url,source,status,salary_range,contact,next_step,notes,fit_score
YYYY-MM-DD,Company,Role Title,URL,source,interested,,,,Score rationale,X/10
```

Use today's date. Status = "interested". NEVER overwrite existing rows. Only append.

### Step 4 — Create Linear Issue (if Linear MCP available)

Check CLAUDE.md for Linear team ID. If available:
- Team: the configured team ID
- Title: [Company] Role Title
- Description: URL, score, key requirements, fit rationale
- Priority: 8-10 = Urgent, 6-7 = High, 4-5 = Normal, 1-3 = Low
- Status: Backlog

If Linear MCP unavailable: skip silently.

### Step 5 — Create TickTick Task (if TickTick MCP available)

Check CLAUDE.md for TickTick project ID. If available:
- Project: the configured project ID
- Title: [X/10] Company — Role Title
- Content: URL + score rationale
- Priority: 8-10 = High (5), 6-7 = Medium (3), 1-5 = Low (1)

If TickTick MCP unavailable: skip silently.

### Step 6 — Present Summary

Show a clean summary:
```
[Company] — Role Title
Location (remote status)
Fit Score: X/10
Rationale: one-line reason
URL: [link]
Added to: CSV | Linear (if available) | TickTick (if available)
```

If multiple inputs were provided, process all and show a summary table at end.

### Step 7 — Persist to Memory

If memory MCP is available, store a memory with:
- Content: "[Company] - [Role] scored [X/10]. [Rationale]"
- Tags: job-intake, [company-name]
