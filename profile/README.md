---

# 🎯 Using This Profile as a Template

**This profile belongs to the original author.** To use Job Search HQ for YOUR job search:

## Quick Start

1. **Delete or replace these files with your own:**
   - `README.md` — your professional summary
   - `cv-scraped.md` — your CV data (or delete if using cv-data.yaml)
   - `linkedin-scraped.md` — your LinkedIn data (or delete)
   - `strengths-summary.md` — your strengths assessment
   - `wolt-capability-digest.md` — your capability examples (delete this)

2. **Keep and customize:**
   - `target-roles.md` — **MOST IMPORTANT!** Your scoring rubric
   - `values.md` — your values and priorities
   - `cv-data.yaml` — structured CV for RenderCV

3. **Optional files to create:**
   - `cover-letter-template.md` — your base cover letter
   - `pitch.md` — your elevator pitch
   - `references.md` — reference contacts

## Customizing target-roles.md

This is the **brain** of the system. The better you define this, the better the AI scores jobs.

### Key Sections to Customize:

**1. Dream Company Tiers**
```markdown
**Tier 0 → floor 8:** Your dream companies (Oxide, Mistral, etc.)
**Tier 1 → floor 7:** Great fits
**Tier 2 → score normally:** Good options
```

**2. Target Roles (Fuzzy Matching)**
```markdown
## Primary Targets
- Senior Product Manager
- Technical Product Manager
- Product Engineer (Oxide model)
- AI Product Lead

## Also Consider
- Staff TPM
- Founding Product role
- Developer Relations (product-focused)
```

**3. Scoring Modifiers**
```markdown
- Remote at remote-first company: +1.5
- Remote-eligible: +1
- Office in [your city]: neutral
- Outside [your country], not remote: cap at 5
- Early-stage (pre-seed/seed): +1 (if you want this)
- AI-native company: +1
- Values-aligned (privacy, open source): +0.5
```

**4. Red Flags (Auto-reject)**
```markdown
- Unpaid "equity-only" roles
- MLM/crypto scams
- "Unlimited vacation" (often means none)
- "Fast-paced startup" (often means chaos)
```

## Example: Adapting for Different Roles

### If You're a Software Engineer:
```markdown
## Target Roles
- Staff Engineer
- Principal Engineer
- Founding Engineer
- Tech Lead

## Scoring Modifiers
- Rust/Go/TypeScript stack: +1
- 10-50 person company: +1
- Open source company: +1
- No on-call: +0.5
```

### If You're a Designer:
```markdown
## Target Roles
- Senior Product Designer
- Design Lead
- Founding Designer

## Scoring Modifiers
- Design-driven company: +1
- Figma-native workflow: +0.5
- User research focus: +1
```

## Tips for Better Scoring

1. **Be specific:** "Series A B2B SaaS" beats "startup"
2. **Use company names:** Tier lists help the AI learn your taste
3. **Include anti-patterns:** "Not: agencies, consultancies, outsourcing"
4. **Update as you learn:** Scored 10 jobs? Refine the rubric.

## Profile Depth = Scoring Quality

The more context you give the AI, the better it scores:

- **Minimal profile** → generic scores (mostly 5-7)
- **Basic profile** → decent scores (4-8 range)
- **Deep profile** → accurate scores (1-10 with confidence)

**Invest in your profile. It's the foundation.**

---


### profile/README.md
```markdown
### profile/README.md
```markdown
1: # Vitalii (Vitalik) Garan — Professional Profile
2: 
3: > *Builder. Generalist. AI-native problem-solver. Refuses to accept "closed without resolution" as an answer.*
4: 
5: ---
6: 
7: ## Identity
8: 
9: Vitalik is not a TPM by training. He's a builder by nature — someone who sees broken systems and fixes them, who gets handed 4 API keys and a blank slate and ships something genuinely impressive.
10: 
11: He grew up as a generalist: equally at home writing Python automation scripts, running a 12-stakeholder program review, drafting an executive update, or architecting a SOX-compliant audit trail. He doesn't want to be put in a box. He wants to build.
12: 
13: His most defining trait is relentlessness. At Wolt, he filed 94 support tickets in 3 months — not as a complaint, but because the systems were broken and he refused to accept dysfunction as a permanent condition. He documented everything, escalated everything, and kept building anyway. When the org responded by treating *him* as the problem rather than fixing their systems, he left with a portfolio of work that speaks for itself.
14: 
15: He treats AI as a first-class collaborator, not a productivity add-on. He has built AI-augmented operating systems, not just used ChatGPT to draft emails. The distinction matters.
16: 
17: **Location:** Frankfurt, Germany (cannot relocate outside Germany)
18: **Target compensation:** 120–160k EUR base + equity
19: **Availability:** Immediate
20: 
21: ---
22: 
23: ## Core Strengths
24: 
25: ### Builder Mindset
26: Vitalik doesn't wait for permission to build things. When no tooling existed, he wrote it. When no process existed, he created it. When no context was being preserved across AI sessions, he built a persistent agent operating system. The output quality of this work — 15+ production-grade Python scripts, a document index covering 1,140 files, a full AI provenance tracking system — is not the output of someone who "uses AI tools." It's the output of someone who thinks in systems.
27: 
28: ### Relentlessness
29: 94 support tickets. A CRM migration delivered on time with zero critical launch bugs. A London workshop with 17 prep files. He doesn't complain about complexity; he maps it, breaks it down, and ships through it. Setbacks are data points, not stopping conditions.
30: 
31: ### Communication & People
32: CliftonStrengths #1: Communication. He is genuinely energized by people — meetings, workshops, cross-functional alignment, stakeholder wrangling. He builds bridges naturally, between teams, between technical and non-technical audiences, between products and the humans who use them. 85th percentile Extroversion. He is not performing enthusiasm — he is actually wired this way.
33: 
34: ### Generalist Range
35: Strategy → execution → tooling → documentation → stakeholder management → technical architecture. He can zoom out to write the roadmap and zoom in to debug the Python script. This is genuinely rare and genuinely valuable in early-stage or fast-moving environments where the job description changes weekly.
36: 
37: ### AI-Native Thinking
38: Vitalik doesn't just prompt. He architects. He built a Git-based agent operating system with persistent context, session protocols, daily digests, and memory across sessions — before most companies had an "AI strategy." He thinks about AI as infrastructure, not a feature.
39: 
40: ---
41: 
42: ## What He Built at Wolt
43: 
44: *Evidence from the Mx-CRM private repository — a genuine technical artifact, not a slide deck.*
45: 
46: ### The AI Agent Operating System
47: Built a private Git repository functioning as a persistent AI agent "OS" — context index, daily digests, session protocols, cross-session memory. Not a prompt library. An actual system for AI-augmented program management that was continuously refined, documented, and used in production. He was actively automating himself out of his own job — and that was the point.
48: 
49: ### Automation Suite (15+ Python Scripts)
50: - **Google Drive sync** — automated document synchronization
51: - **Confluence auto-publishing** — programmatic documentation delivery
52: - **Glean enterprise search CLI** — custom search tool with filters, multi-channel OR queries, JSON output. Built because the GUI wasn't good enough.
53: - **Document registry builder** — crawled and classified 1,140 documents across Drive/Confluence/Jira/Slack
54: - **Preflight auth checker** — validated credentials and service connectivity before run-time failures
55: - **Google write guardrails** — environment-variable-gated write protection to prevent accidental document corruption
56: - **AI provenance tracking** — every AI-created document in Drive and Confluence carries an agent marker. Full audit trail.
57: 
58: ### CRM Migration (Pipedrive → Salesforce)
59: Delivered for ~50 Account Managers across Finland and Denmark. On schedule. Zero critical launch bugs. Managed across Engineering, Product, Sales Operations, and Business Support teams — 12+ stakeholders, 3 parallel workstreams. SOX-compliant commission change architecture with MongoDB audit logging.
60: 
61: ### London Pedregal Workshop
62: Led end-to-end: 17 preparation files, 7 session note files. A complex cross-functional alignment event, delivered.
63: 
64: ### The Environment Context
65: Wolt post-DoorDash acquisition was political chaos. Staff TPMs were burnt out and turf-protecting. The IT org optimized for ticket closure, not problem resolution — his 94 tickets were treated as *his* problem, not the system's. "Holocratic" culture was a facade; decisions happened in hallways. He was eventually let go without direct conversation from his hiring manager.
66: 
67: Frame this correctly: it was a mismatch between an activator-builder and a compliance-first bureaucracy mid-M&A meltdown. The work he produced in that environment is more impressive, not less, given those conditions.
68: 
69: ---
70: 
71: ## Career Highlights
72: 
73: ### Ring (Amazon) — Senior Technical Program Manager
74: Led the **Ring Ultra radar camera** from zero to production. Coordinated 10+ teams across 5 locations, 400+ people. ~800,000 units sold at launch.
75: 
76: Rolled out **People-Only Mode (Motion Settings 2.0)** to 40M+ devices — phased release at 1 million devices per day. Zero-defect rollout at that scale requires airtight coordination, clear communication, and deep cross-functional trust. He built all three.
77: 
78: ### CloudMade — Technical Program / Business Development
79: Built the **Experience Car demo program** from the ground up: 5 demo cars deployed worldwide, 200+ demo drives conducted, several $1M+ contracts directly attributed. Turned a product concept into a tangible, revenue-generating sales motion.
80: 
81: ---
82: 
83: ## Assessments
84: 
85: | Assessment | Result |
86: |---|---|
87: | **CliftonStrengths Top 5** | Communication, Ideation, Strategic, Responsibility, Activator |
88: | **EPP Self-Confidence** | 89th percentile |
89: | **EPP Extroversion** | 85th percentile |
90: | **EPP Openness** | 83rd percentile |
91: | **EPP Management & Leadership match** | 90% |
92: | **CCAT Overall** | 71st percentile |
93: | **CCAT Spatial Reasoning** | 90th percentile |
94: | **CCAT Math / Logic** | 85th percentile |
95: 
96: The pattern: high communication, high confidence, high openness, strong spatial and logical reasoning. This is a person who can hold complexity, communicate clearly, and move fast. The Activator strength is load-bearing — he starts things, he doesn't wait.
97: 
98: ---
99: 
100: ## What He's Looking For
101: 
102: Vitalik is not looking for a classic TPM role. He's looking for a place to grow into an AI engineer / general builder.
103: 
104: **The right company:**
105: - Lovable, Mistral, Oxide Computer, Replit, Modal — places where *shipping* is the culture
106: - AI-native orgs where his ability to build with AI is a feature, not a curiosity
107: - Early-stage or growth-stage teams where generalists are valued over specialists
108: - Companies with a builder culture: fewer slide decks, more pull requests
109: 
110: **The right role:**
111: - AI engineer, product engineer, technical PM with real engineering adjacency
112: - Roles where building tools, pipelines, and integrations is the job
113: - Environments where autonomy is high and process is lean
114: - A clear path toward growing into engineering — not staying in program management forever
115: 
116: **What he brings:**
117: - Unusually broad range — strategy to code to communication to execution
118: - AI system building (not just AI tool usage)
119: - Track record of delivery in complex, multi-stakeholder environments
120: - Energy and positivity that is genuine, not performed
121: - The ability to walk into ambiguity and create structure
122: 
123: ---
124: 
125: ## Hard Nos (Anti-Patterns)
126: 
127: These are environments where Vitalik will underperform or leave quickly:
128: 
129: - **PMBOK-heavy process roles** — process for process's sake drains him
130: - **Bureaucratic orgs where "AI strategy" is a slide deck** — he needs to actually build
131: - **Organizations that fear change** — Wolt was the archetype; he needs the opposite
132: - **Roles with no trajectory toward building / engineering** — staying purely in program management is not the goal
133: - **Environments where being the smartest person in the room is threatening** — he needs peers who are excited to collaborate, not protect territory
134: - **Companies outside Germany** — he is in Frankfurt and cannot relocate
135: 
136: ---
137: 
138: ## The Summary (one paragraph)
139: 
140: Vitalik is a relentless, energetic, AI-native builder who happens to have a TPM background. He's technically credible — not in the sense of writing production Java, but in the sense of architecting systems, building automation pipelines, and thinking clearly about how software works. He's a generalist in the best sense: he can go wide and go deep, switch between strategy and execution, and communicate effectively with engineers, executives, and everyone in between. He is looking for an environment that celebrates builders, values range, and has the ambition to build things that matter. Given the right environment, he will be one of the most productive and energizing people on the team.
```
```
```
