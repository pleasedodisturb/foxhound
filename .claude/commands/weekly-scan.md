Run an automated weekly job scan. Search all sources, score results, and produce a digest file. No interactive prompts — make all decisions automatically based on profile/target-roles.md.

## Input

$ARGUMENTS

Optional: min_score (default: 6), hours_old (default: 168 = 1 week).

## Instructions

Read `AGENT.md` and `profile/target-roles.md` before starting.

### Search — same sources as /job-discover but with wider time window

#### JobSpy MCP (if available)

Run all search terms from your profile with hours_old: 168 (1 week) and results_wanted: 30.

#### Local Job APIs

Run: `.venv/bin/python tools/germany_jobs.py --preset all --limit 25 --output json`

Adapt to your regional tools.

#### Himalayas MCP (if available)

Search all target role terms for remote positions.

#### Web Search

Search for recent postings matching target roles.

### Auto-score everything

Score all results against `profile/target-roles.md`.
Only keep scores >= min_score (default: 6).

### Skip if already tracked

Read `tracking/applications.csv`. Skip any job where company + role already exists in CSV.

### Output digest

Write to `tracking/weekly-scan-YYYY-MM-DD.md`:

```markdown
# Weekly Job Scan — YYYY-MM-DD

## New Roles Found (score >= N, not yet tracked)
| Score | Company | Role | Location | Source | URL |

## Stats
- Total searched: N
- Scored >= threshold: N
- Already tracked: N
- New this week: N

## Quick adds (copy-paste for /job-intake)
[URLs of top 5 by score]
```

Do NOT auto-add to CSV or task managers — present digest for human review.

Save the digest file, then print a summary.

### Persist to Memory

If memory MCP is available, store a memory with:
- Content: "Weekly scan [date]: [N] new roles found, top score [X/10] at [Company]"
- Tags: weekly-scan, discovery
