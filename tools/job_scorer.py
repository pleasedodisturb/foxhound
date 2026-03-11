"""
Score scraped job listings against profile criteria using OpenAI.

Usage:
    export OPENAI_API_KEY=your_key
    python tools/job_scorer.py tracking/scraped_jobs_2026-02-22.csv

Reads scraped jobs CSV, scores each against the ideal role profile,
and writes results with fit_score, fit_reasoning, estimated_salary,
effort_flag, prep_level, and prep_notes columns.
"""

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

PROFILE_CRITERIA = """
Ideal candidate profile for job scoring:

MUST-HAVES (weight heavily):
- AI/ML focus or genuine openness to AI integration
- High autonomy and freedom to choose tools/approaches
- Strategic thinking valued over process compliance
- Complex problems, not administrative busywork
- Leadership or senior IC role

STRONG POSITIVES:
- Remote-friendly or based in your target city
- Equity/RSU component
- Startup or scale-up environment
- Building things, not just reporting on them
- Cross-functional collaboration
- Innovation mandate with executive sponsorship

RED FLAGS (score down):
- Heavy PMBOK/PMO process language
- "Coordinate meetings" as primary responsibility
- No mention of AI or technology innovation
- Very rigid hierarchy descriptions
- "Must have 10+ years in [narrow specialty]"

SALARY & EFFORT CONTEXT:
- Target: [your salary range]. Below [floor] is a dealbreaker unless exceptional trajectory.
- Sweet spot: [your ideal level/stage] (stable, reasonable hours, real equity).
- Market bands: customize per your location and seniority.
- Remote-first international companies typically pay 15-30% above local market.
- If salary not posted, estimate based on company stage, role level, and location.
# TODO: Customize salary bands and floor to match your profile/target-roles.md

SALARY SCORING:
- Include 'estimated_salary' (string, e.g. "110-130k EUR") in your response.
- Include 'effort_flag' (string: "sweet-spot", "moderate", "high-intensity", "unknown").

PREPARATION TOUGHNESS:
- Include 'prep_level' (integer 1-5):
  1 = wing it (your background is a direct match)
  2 = light prep (brush up on a few topics)
  3 = moderate (need to study specific domain/tools)
  4 = heavy (significant gaps to close)
  5 = new domain (would need to learn fundamentals)
- Include 'prep_notes' (string, one sentence explaining what prep is needed).
"""


def score_job(
    client, title: str, company: str, description: str
) -> tuple[int, str, str, str, int, str]:
    """Score a single job posting. Returns (score, reasoning, estimated_salary, effort_flag, prep_level, prep_notes)."""
    if not description or pd.isna(description):
        return 0, "No description available", "unknown", "unknown", 0, "unknown"

    desc_truncated = description[:3000]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a job fit evaluator. Score the job posting against the candidate profile "
                    "on a scale of 1-10. Return ONLY a JSON object with these fields: "
                    "'score' (integer), 'reasoning' (one sentence), "
                    "'estimated_salary' (string, e.g. '110-130k EUR'), "
                    "'effort_flag' (string: 'sweet-spot', 'moderate', 'high-intensity', or 'unknown'), "
                    "'prep_level' (integer 1-5), 'prep_notes' (one sentence). "
                    "No markdown."
                ),
            },
            {
                "role": "user",
                "content": f"CANDIDATE PROFILE:\n{PROFILE_CRITERIA}\n\nJOB POSTING:\nTitle: {title}\nCompany: {company}\nDescription: {desc_truncated}",
            },
        ],
        temperature=0.3,
    )

    import json

    try:
        result = json.loads(response.choices[0].message.content)
        return (
            int(result["score"]),
            result["reasoning"],
            result.get("estimated_salary", "unknown"),
            result.get("effort_flag", "unknown"),
            int(result.get("prep_level", 0)),
            result.get("prep_notes", "unknown"),
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return 5, f"Parse error: {response.choices[0].message.content[:100]}", "unknown", "unknown", 0, "unknown"


def main():
    parser = argparse.ArgumentParser(description="Score job listings against profile")
    parser.add_argument("csv_path", help="Path to scraped jobs CSV")
    parser.add_argument("--limit", type=int, help="Max jobs to score (for cost control)")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        sys.exit(1)

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    if args.limit:
        df = df.head(args.limit)

    print(f"Scoring {len(df)} jobs...")
    scores = []
    reasonings = []
    salaries = []
    efforts = []
    prep_levels = []
    prep_notes_list = []

    for i, row in df.iterrows():
        title = row.get("title", "Unknown")
        company = row.get("company", "Unknown")
        description = row.get("description", "")
        score, reasoning, salary, effort, prep, prep_notes = score_job(
            client, title, company, description
        )
        scores.append(score)
        reasonings.append(reasoning)
        salaries.append(salary)
        efforts.append(effort)
        prep_levels.append(prep)
        prep_notes_list.append(prep_notes)
        print(f"  [{score}/10] {title} @ {company} | {salary} | effort:{effort} | prep:{prep}/5 -- {reasoning}")

    df["fit_score"] = scores
    df["fit_reasoning"] = reasonings
    df["estimated_salary"] = salaries
    df["effort_flag"] = efforts
    df["prep_level"] = prep_levels
    df["prep_notes"] = prep_notes_list

    output_path = csv_path.with_stem(csv_path.stem + "_scored")
    df.to_csv(output_path, index=False)
    print(f"\nSaved scored results to {output_path}")

    top = df.nlargest(10, "fit_score")
    print("\nTop 10 matches:")
    for _, row in top.iterrows():
        print(f"  [{row['fit_score']}/10] {row.get('title', '?')} @ {row.get('company', '?')} | {row.get('estimated_salary', '?')} | prep:{row.get('prep_level', '?')}/5")


if __name__ == "__main__":
    main()
