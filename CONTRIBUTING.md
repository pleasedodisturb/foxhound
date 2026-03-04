# Contributing to Job Search HQ

Thank you for your interest in improving Job Search HQ! 🎉

This is a personal operations system, but contributions are welcome to make it better for everyone.

---

## 🎯 Areas for Contribution

### 1. **New Job Sources**

Add scrapers or API integrations for:
- Niche job boards (ProductHunt, AngelList, YC jobs)
- Company-specific career pages (Stripe, GitHub, etc.)
- Regional boards (Europe, Asia, etc.)
- Industry-specific (AI/ML, DevTools, etc.)

**Where to add:** `tools/` directory

**Example:** See `tools/germany_jobs.py` for reference

### 2. **Better Scoring**

Improve the scoring algorithm:
- ML-based preference learning
- Sentiment analysis of job descriptions
- Salary band estimation
- Company culture signals

**Where to edit:** `tools/job_scorer.py`

### 3. **Dashboard Features**

Add visualizations and features:
- Timeline view
- Conversion funnel
- Salary comparison
- Network graph (who works where)
- Export to Notion/Airtable

**Where to add:** `dashboard/src/`

### 4. **Documentation**

Improve guides:
- Video tutorials
- More use cases
- Troubleshooting
- Non-technical setup guide

**Where to edit:** `docs/` or root `.md` files

### 5. **Goose Recipes**

Add new workflows:
- Interview prep mode
- Offer comparison
- Automated follow-ups
- Company research

**Where to add:** `recipes/`

---

## 🛠️ Development Setup

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/job-search-hq.git
cd job-search-hq
```

### 2. Setup Environment

```bash
# Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Dashboard
cd dashboard
npm install
cd ..
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

- Write code
- Test locally
- Update docs if needed

### 5. Submit PR

```bash
git add .
git commit -m "Add: description of your change"
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

---

## 📋 Code Style

### Python

- **Style:** PEP 8
- **Type hints:** Use where reasonable
- **Docstrings:** For public functions
- **Linting:** `black` formatter (if installed)

**Example:**

```python
def score_job(job_description: str, profile: dict) -> int:
    """
    Score a job posting against user profile.
    
    Args:
        job_description: Full text of job posting
        profile: User profile dict from target-roles.md
        
    Returns:
        Score from 1-10
    """
    # Implementation
    return score
```

### TypeScript (Dashboard)

- **Style:** ESLint + Prettier defaults
- **Types:** Strict mode
- **Components:** Functional + hooks
- **Naming:** PascalCase for components, camelCase for functions

**Example:**

```typescript
interface JobApplication {
  company: string;
  role: string;
  score: number;
}

export function JobCard({ job }: { job: JobApplication }) {
  return <div>{job.company}</div>;
}
```

### Goose Recipes

- **Format:** YAML
- **Naming:** kebab-case
- **Comments:** Explain non-obvious steps

**Example:**

```yaml
name: Job Intake
description: Process a job posting URL
steps:
  - action: fetch_posting
    description: Scrape job description
  - action: score_job
    description: Score 1-10 against profile
  - action: add_to_csv
    description: Append to tracking/applications.csv
```

---

## 🧪 Testing

### Python Scripts

```bash
# Manual testing
python tools/germany_jobs.py --preset test
python tools/job_scorer.py --job-url "https://..." --verbose
```

**Recommended:**
- Unit tests (pytest)
- Integration tests for API calls
- Mock external dependencies

### Dashboard

```bash
cd dashboard
npm run dev
# Open http://localhost:3000 and test manually
```

**Recommended:**
- Component tests (Jest + React Testing Library)
- E2E tests (Playwright)

### Goose Recipes

```bash
goose session start
# Test the recipe interactively
```

---

## 📝 Commit Message Guidelines

Use conventional commits:

```
feat: Add LinkedIn scraper
fix: Correct scoring logic for remote jobs
docs: Update SETUP.md with Node.js requirement
style: Format germany_jobs.py with black
refactor: Extract scoring logic to separate module
test: Add unit tests for job_scorer
chore: Update dependencies
```

**Format:**

```
type: Short description (50 chars max)

Longer explanation if needed (wrap at 72 chars).
Can include multiple paragraphs.

- Bullet points are fine
- Reference issues: Fixes #123
```

---

## 🚫 What NOT to Contribute

### ❌ Personal Data

- Real application CSVs
- Personal contact info
- API keys
- Company-specific documents

### ❌ Out-of-Scope Features

- Full ATS (applicant tracking system)
- CRM features (contact management)
- Social media automation
- Job post scraping that violates ToS

### ❌ Breaking Changes

- Changing CSV schema without migration script
- Removing existing features without deprecation
- Breaking Goose recipe compatibility

**Discuss big changes in an issue first!**

---

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in docs

**Thank you for making this better!** 🙏

---

## 📞 Questions?

- Open an issue (preferred)
- Start a discussion
- Comment on relevant issues

**Let's build something useful together.** 🚀
