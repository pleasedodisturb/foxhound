"""Shared fixtures for all tests."""

import sys
from pathlib import Path

import pytest

# Ensure tools/ is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))


@pytest.fixture
def sample_jobs():
    """Sample job dicts for testing pipeline steps."""
    return [
        {
            "title": "Senior AI Product Manager",
            "company": "Mistral AI",
            "location": "Remote, EU",
            "url": "https://mistral.ai/careers/pm",
            "source": "remotive",
            "description": "Build AI products with autonomy. ML platform team.",
            "posted": "2026-03-10",
            "remote": True,
            "salary": "130-160k EUR",
            "tags": ["ai", "product"],
            "fit_score": 9,
            "fit_reasoning": "Strong AI focus, remote, builder role",
            "estimated_salary": "130-160k EUR",
            "effort_flag": "sweet-spot",
            "prep_level": 2,
            "prep_notes": "Brush up on LLM deployment",
        },
        {
            "title": "Technical Program Manager",
            "company": "Linear",
            "location": "Remote",
            "url": "https://linear.app/jobs/tpm",
            "source": "weworkremotely",
            "description": "Coordinate technical programs for developer tools.",
            "posted": "2026-03-09",
            "remote": True,
            "salary": "",
            "tags": ["tpm"],
            "fit_score": 7,
            "fit_reasoning": "Good company, builder culture",
            "estimated_salary": "120-140k EUR",
            "effort_flag": "moderate",
            "prep_level": 2,
            "prep_notes": "Study Linear's product",
        },
        {
            "title": "PMO Coordinator",
            "company": "Big Corp AG",
            "location": "Munich, Germany",
            "url": "https://bigcorp.de/jobs/pmo",
            "source": "arbeitsagentur",
            "description": "PMBOK-based project coordination. Administrative tasks.",
            "posted": "2026-03-08",
            "remote": False,
            "salary": "",
            "tags": [],
            "fit_score": 2,
            "fit_reasoning": "PMBOK-heavy, no AI, not remote",
            "estimated_salary": "70-85k EUR",
            "effort_flag": "high-intensity",
            "prep_level": 1,
            "prep_notes": "N/A",
        },
        {
            "title": "AI Engineer",
            "company": "Startup GmbH",
            "location": "Berlin, Germany",
            "url": "https://startup.de/ai",
            "source": "germantechjobs",
            "description": "Founding AI engineer. Build ML pipelines.",
            "posted": "2026-03-10",
            "remote": False,
            "salary": "90-110k EUR",
            "tags": ["ai", "ml", "founding"],
            "fit_score": 6,
            "fit_reasoning": "AI focus, founding team, but not remote",
            "estimated_salary": "90-110k EUR",
            "effort_flag": "moderate",
            "prep_level": 4,
            "prep_notes": "Need to ramp up on MLOps",
        },
    ]


@pytest.fixture
def tmp_tracking_dir(tmp_path):
    """Create a temporary tracking directory with sample CSV."""
    tracking = tmp_path / "tracking"
    tracking.mkdir()

    csv_content = (
        "date_applied,company,role,url,source,status,salary_range,contact,next_step,notes,fit_score\n"
        '2026-03-01,Existing Co,Senior PM,https://example.com,linkedin,interested,"100-120k",,,Good fit,7/10\n'
        '2026-03-05,Another Inc,AI Lead,https://another.com,indeed,applied,"130-150k",,,Strong AI,8/10\n'
    )
    (tracking / "applications.csv").write_text(csv_content)

    return tracking
