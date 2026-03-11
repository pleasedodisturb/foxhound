# Tracking

This directory contains your job application log and supporting data.

## Files

| File | Description |
|------|-------------|
| `applications.csv` | **Your personal application log** — not committed to git |
| `applications.csv.example` | Example format with fake data — use as a template |

## Getting Started

```bash
# Copy the example to create your personal log
cp tracking/applications.csv.example tracking/applications.csv
```

Your `applications.csv` is gitignored — it stays on your machine. Never commit real application data.

## CSV Schema

```
date_applied,company,role,url,source,status,salary_range,contact,next_step,notes,fit_score
```

| Column | Description | Example |
|--------|-------------|---------|
| `date_applied` | Date added (YYYY-MM-DD) | `2026-01-15` |
| `company` | Company name | `Mistral AI` |
| `role` | Full role title | `AI Product Manager` |
| `url` | Job posting URL | `https://mistral.ai/jobs/...` |
| `source` | Where you found it | `linkedin` / `indeed` / `company` |
| `status` | Current status | See below |
| `salary_range` | If listed in JD | `120k-150k EUR` |
| `contact` | Recruiter/HM name | `Jane Smith` |
| `next_step` | What to do next | `Follow up by Jan 20` |
| `notes` | AI score rationale + your notes | `Strong AI focus, remote-first` |
| `fit_score` | AI score 1-10 | `8/10` |

## Status Values

| Status | Meaning |
|--------|---------|
| `interested` | Saved, not yet applied |
| `applied` | Application submitted |
| `interviewing` | In process |
| `offered` | Offer received |
| `rejected` | Not selected |
| `withdrawn` | You withdrew |
| `ghosted` | No response after follow-up |

## Tips

- **Let the AI fill it**: Use the `job-intake` recipe — it appends rows automatically
- **Never manually sort/reorder**: Append-only keeps a clean history
- **Add notes liberally**: "Why did I save this?" context is valuable later
- **Review weekly**: Move statuses, add next steps, prune dead ends
