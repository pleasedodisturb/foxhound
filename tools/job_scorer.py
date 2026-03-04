"""
Score scraped job listings against profile criteria using OpenAI.

Usage:
    export OPENAI_API_KEY=your_key
    python tools/job_scorer.py tracking/scraped_jobs_2026-02-22.csv

Reads scraped jobs CSV, scores each against the ideal role profile,
and writes results with fit_score and fit_reasoning columns.
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
- Remote-friendly or Frankfurt-based
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

SALARY CONTEXT: Target 120-160k EUR base. Below 100k is a dealbreaker.
"""


def score_job(client, title: str, company: str, description: str) -> tuple[int, str]:
    """Score a single job posting. Returns (score 1-10, reasoning)."""
    if not description or pd.isna(description):
        return 0, "No description available"

    desc_truncated = description[:3000]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a job fit evaluator. Score the job posting against the candidate profile "
                    "on a scale of 1-10. Return ONLY a JSON object with 'score' (integer) and "
                    "'reasoning' (one sentence). No markdown."
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
        return int(result["score"]), result["reasoning"]
    except (json.JSONDecodeError, KeyError, ValueError):
        return 5, f"Parse error: {response.choices[0].message.content[:100]}"


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

    for i, row in df.iterrows():
        title = row.get("title", "Unknown")
        company = row.get("company", "Unknown")
        description = row.get("description", "")
        score, reasoning = score_job(client, title, company, description)
        scores.append(score)
        reasonings.append(reasoning)
        print(f"  [{score}/10] {title} @ {company} -- {reasoning}")

    df["fit_score"] = scores
    df["fit_reasoning"] = reasonings

    output_path = csv_path.with_stem(csv_path.stem + "_scored")
    df.to_csv(output_path, index=False)
    print(f"\nSaved scored results to {output_path}")

    top = df.nlargest(10, "fit_score")
    print("\nTop 10 matches:")
    for _, row in top.iterrows():
        print(f"  [{row['fit_score']}/10] {row.get('title', '?')} @ {row.get('company', '?')}")


if __name__ == "__main__":
    main()
