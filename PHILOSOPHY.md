# Philosophy — Why Job Search HQ Exists

This document explains the **why** behind the system — the thinking, the pain points, and the builder's approach to solving them.

---

## 🔥 The Problem

**Job searching is broken.**

Not because there aren't enough jobs, but because:

1. **Noise >> Signal**
   - 100s of job posts, 3 are relevant
   - LinkedIn spam, recruiter spam, automated outreach
   - Most "matches" are keyword collisions, not real fits

2. **Tools Optimize for Volume, Not Quality**
   - Job boards want you to apply to more jobs (more data for them)
   - LinkedIn wants you to scroll more (more ads)
   - No tool helps you think: "Is this actually good for me?"

3. **Manual Tracking is Soul-Crushing**
   - Spreadsheets get stale
   - No context recall ("Wait, why did I save this?")
   - Copy-pasting URLs, dates, notes — busywork

4. **Generic CVs Lose to Tailored Ones**
   - One CV for 50 jobs = rejection
   - Tailoring by hand = 2 hours per application
   - No one has time for that

5. **The Paradox of Choice**
   - More options → worse decisions
   - Decision fatigue → applying randomly
   - No framework = chaos

**This is not a tools problem. It's a system problem.**

---

## 💡 The Insight

**Job search is an operations problem, not a discovery problem.**

What if you treated job search like building a product?

- **Define your ICP (Ideal Company Profile)** → `profile/target-roles.md`
- **Automate the pipeline** → Goose recipes, MCP integrations
- **Score leads** → 1-10 system, not binary yes/no
- **Track in a CRM** → CSV + dashboard, not chaos
- **Measure & iterate** → conversion rates, bottlenecks

**This is Job Search as a System.**

---

## 🎯 Design Philosophy

### 1. AI-Native, Not AI-Augmented

Most "AI job search tools" are:
- Traditional scrapers + ChatGPT wrapper
- "AI resume builder" = templates with GPT text fill
- Thin value add

**Job Search HQ is different:**
- AI is the **orchestration layer** (Goose)
- AI is the **scoring engine** (fuzzy matching, context-aware)
- AI is the **memory layer** (ContextStream)

AI is **infrastructure**, not a feature.

### 2. Context-Rich, Not Rule-Based

Traditional systems:
- "Filter by: salary, location, title"
- Rigid, brittle, misses nuance

**Job Search HQ:**
- Deep profile → AI understands intent
- Fuzzy scoring → "this feels like X"
- Values-aware → "not just any job, the right job"

Example:
- Rule-based: "Title must contain 'Product Manager'"
- Context-rich: "This is a PM role even though it's called 'Product Engineer' because the JD is 90% PM work"

### 3. Local-First, Cloud-Optional

Your job search data is **yours**:
- Sensitive (companies, contacts, notes)
- Permanent (you'll want this in 5 years)
- Portable (switch tools anytime)

**Design:**
- CSV = canonical source of truth (local)
- Git = version control (local)
- Markdown = all docs (local, readable)
- Cloud integrations = opt-in (Linear, TickTick)

**You own the data. The system serves you.**

### 4. Human-in-the-Loop, AI-Executes

AI is **not** autonomous here:
- AI discovers → you decide
- AI scores → you override
- AI drafts → you edit
- AI suggests → you approve

**Why?**
- Job search is high-stakes
- You have context AI doesn't
- Trust is earned, not assumed

**Workflow:**
- Goose: "Found 10 jobs, top 3 scored 8+. Want details?"
- You: "Show me #1 and #3"
- Goose: "Here's the breakdown. Apply to #1?"
- You: "Yes, draft cover letter"
- Goose: "Here's the draft. Edits?"

**AI accelerates. You decide.**

### 5. Systems Thinking Over Tools

Most people job search like this:
1. See job post
2. Apply or skip
3. Repeat

**This is reactive, chaotic, exhausting.**

**Job Search HQ is proactive:**
1. Define what you want (`profile/`)
2. Set up discovery pipelines (`tools/`, MCP)
3. Process inbound jobs systematically (`recipes/`)
4. Track everything (`tracking/`)
5. Measure & iterate (dashboard)

**You're not just applying. You're operating.**

---

## 🧠 The Builder's Mindset

### Why I Built This

**Personal context:**

I got fired from Wolt. The org was in post-M&A chaos. I built an AI-augmented TPM system in a hostile environment — burnt-out team, political culture, systems that closed tickets without fixing problems.

**I was relentless. They called it a problem.**

The right environment would call it **operational excellence**.

**So I built this to:**
1. **Prove I can ship** — not just manage, but build
2. **Showcase systems thinking** — this repo is the portfolio
3. **Find the right fit** — not any job, the right one
4. **Operate like a founder** — even in personal projects

### Why You Might Build This

You should fork this if:

- You're a **builder** looking for a builder-friendly company
- You're **picky** (high bar, not desperate)
- You're **technical enough** to run Python/Node.js
- You want to **own your process**, not rent it from LinkedIn
- You believe **systems > heroics**

**If you're applying to 100 jobs/week, this is not for you.**
This is for people who apply to 5 jobs/month and nail every one.

---

## 🎨 Influences & Inspiration

### 1. **Oxide Computer Company**

Their "[product engineer](https://oxide.computer/careers)" model:
- No PM/Eng split
- You build what you spec
- Deep technical + product thinking

**Why relevant:**
- This repo is a product (not just a tool)
- I'm not a "just PM" or "just engineer"
- I want to work at companies that blur these lines

### 2. **Stripe's "Own Your Career" Ethos**

Stripe publishes:
- Career ladders (internal docs)
- Interview prep guides
- Transparent comp bands

**Why relevant:**
- Transparency breeds better decisions
- This repo is radically transparent (you see my rubric!)
- High-trust orgs share context

### 3. **GitLab's Handbook-First Culture**

Everything is documented:
- Values, processes, decisions
- Async-first, remote-first
- Public by default

**Why relevant:**
- This repo is my "handbook"
- It's how I'd run a team
- Shows my thinking, not just outputs

### 4. **Goose (Block's AI Executor)**

Goose represents:
- AI as infrastructure
- Developers as orchestrators
- Context-aware automation

**Why relevant:**
- I'm not just using Goose, I'm showcasing how
- This is AI-native operations in action
- Block (Square, CashApp) gets it

---

## 🚫 What This Is NOT

### ❌ Not a "Spray and Pray" Tool

If you want to apply to 100 jobs/week, use:
- LinkedIn Easy Apply
- ZipRecruiter
- Indeed

This is the **opposite** of that.

### ❌ Not a Job Board

This doesn't have its own job listings. It **aggregates** from:
- JobSpy (Indeed, LinkedIn, Glassdoor)
- Arbeitsagentur (Germany)
- Brave Search (company career pages)
- Your manual inputs

### ❌ Not a "Get Rich Quick" Career Tool

This won't:
- Magically get you interviews
- Write perfect cover letters
- Game ATS systems
- Guarantee offers

**It will:**
- Help you find the right opportunities
- Save you time on busywork
- Make better decisions faster
- Track your progress

### ❌ Not a Product (Yet)

This is a **personal project**, open-sourced.

It's not:
- A SaaS
- A startup
- Monetized

**It's a portfolio piece + tool I actually use.**

If it becomes a product someday, great. For now, it's proof of concept.

---

## 🌍 Who This Is For

### Ideal User Profile

- **Role:** Senior IC or early manager (Staff Eng, Principal PM, Founding Engineer)
- **Stage:** Not desperate, but actively looking
- **Pickiness:** High bar (would rather wait than settle)
- **Technical:** Comfortable with CLI, Python, Node.js
- **Mindset:** Builder, systems thinker, AI-curious

**Example personas:**
- Staff Engineer at FAANG → wants to join early-stage AI startup
- TPM at enterprise → wants to build at remote-first product company
- Senior PM → wants Product Engineer role at Oxide-like company
- Founding Engineer → wants AI-focused builder role

### Not For

- Entry-level (this is overkill)
- Non-technical (too much setup)
- Desperate (this is slow, methodical)
- Volume-oriented (this is quality-focused)

---

## 🔮 Future Vision

### Short-Term: Personal Tool

Right now, this is:
- My job search system
- Open-sourced for others
- A portfolio showcase

### Medium-Term: Community Tool

Could become:
- Goose extension marketplace item
- MCP server collection
- Shared rubrics/profiles
- Community-contributed job sources

### Long-Term: Platform?

Maybe:
- SaaS for power users
- Team version (hiring pipelines)
- Marketplace (sell your rubric/system)
- AI copilot for career ops

**But that's speculation.** For now, it's a tool I use.

---

## 📚 Lessons Learned

### What Worked

- **CSV is good enough** — no need for a database yet
- **Goose recipes** — repeatable workflows are gold
- **Deep profile** — the better your rubric, the better the AI scores
- **Scoring > filtering** — 1-10 beats binary yes/no
- **Local-first** — owning data feels right

### What Didn't

- **Over-automation** — tried to auto-apply, way too risky
- **Too many integrations** — started with 10, narrowed to 3
- **Perfect CV** — good enough beats perfect-but-late
- **Rigid filters** — fuzzy matching is way better

### What I'd Do Differently

- Start with CSV + CLI, add dashboard later
- Build profile first, code second
- Test scoring on 10 jobs before automating
- Document as I go (not retroactively)

---

## 🤝 Open Source Ethos

### Why Share This?

1. **Transparency** — shows my thinking
2. **Portfolio** — this is the work
3. **Community** — others might improve it
4. **Learning** — teaching is the best way to learn

### How to Contribute

See `CONTRIBUTING.md`. Key areas:
- New job sources (APIs, scrapers)
- Better scoring algorithms
- Dashboard features
- Documentation

### License

MIT — do whatever you want with this.

**But if you:**
- Land a job using this → tell me!
- Improve it → contribute back
- Build something cool → share it

---

## 💬 Final Thoughts

**Job search doesn't have to suck.**

It sucks because we treat it like a chore, not a system.

**This repo is my answer:**
- Systems thinking applied to personal operations
- AI as infrastructure, not magic
- Builder mindset in action

**If you're reading this, you're probably like me:**
- You don't want just any job
- You want the right one
- You're willing to build tools to find it

**Welcome.**

---

**Questions? Thoughts? Ideas?**

Open an issue, start a discussion, or fork and make it yours.

**Happy hunting.**

— *A builder in search of the right environment*
