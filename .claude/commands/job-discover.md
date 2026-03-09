Search for jobs across all available sources, score against profile, and present a ranked table.

## Input

$ARGUMENTS

Optional: override keywords or filters. If empty, runs the full preset search from profile/target-roles.md.

## Instructions

Read `AGENT.md` and `profile/target-roles.md` before starting.

### Search Strategy — run ALL available sources, then deduplicate

#### 1. JobSpy MCP (if available)

Use the search_jobs tool with these searches (adapt terms to your profile/target-roles.md):
- search_term: "AI Product Manager", site_names: "linkedin,indeed", results_wanted: 25, hours_old: 72
- search_term: "Technical Program Manager AI", site_names: "linkedin,indeed", results_wanted: 25, hours_old: 72
- search_term: "Product Engineer AI", site_names: "linkedin,indeed", results_wanted: 20, hours_old: 72, is_remote: true
- search_term: "AI Engineer product", site_names: "linkedin,indeed", results_wanted: 20, hours_old: 72
- search_term: "Technical Product Manager developer tools", site_names: "linkedin", results_wanted: 20, hours_old: 72

Set location and country filters from your profile.

#### 2. Local Job APIs

Run: `.venv/bin/python tools/germany_jobs.py --preset all --location "[Your City]" --limit 20 --output json`

Adapt the script and location to your regional job boards.

#### 3. Web Search

Use WebSearch to find recent postings on company career pages matching your target roles.

#### 4. Himalayas MCP (if available)

Search for remote-only roles matching your profile keywords.

### Scoring

Score ALL results against `profile/target-roles.md`. Apply the full scoring rubric from AGENT.md.

### Deduplication

Remove duplicates by (company + role title). Keep highest score version.

### Filters — skip these

- Roles requiring 5+ years in a specific domain you lack
- Junior roles or roles requiring < 3 years experience
- Roles clearly outside your country with no remote option

### Output

Present a ranked table sorted by score descending:

```
| # | Score | Company | Role | Location | Remote | Source | URL |
```

Then ask: "Which roles do you want to add to tracking? (enter numbers, e.g. 1,3,5 or 'all')"

For each selected role, run the job-intake workflow (Steps 3-7 from /job-intake).
