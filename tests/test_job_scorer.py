"""Tests for tools/job_scorer.py — AI-based job scoring."""

import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from job_scorer import PROFILE_CRITERIA, score_job


# ==================== PROFILE_CRITERIA ====================


class TestProfileCriteria:
    def test_criteria_is_nonempty(self):
        assert len(PROFILE_CRITERIA) > 100

    def test_contains_must_haves(self):
        assert "MUST-HAVES" in PROFILE_CRITERIA

    def test_contains_scoring_instructions(self):
        assert "fit_score" in PROFILE_CRITERIA or "score" in PROFILE_CRITERIA.lower()

    def test_contains_effort_flag(self):
        assert "effort_flag" in PROFILE_CRITERIA

    def test_contains_prep_level(self):
        assert "prep_level" in PROFILE_CRITERIA


# ==================== score_job ====================


class TestScoreJob:
    def _make_client(self, response_json: dict):
        """Create a mock OpenAI client that returns the given JSON."""
        client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(response_json)
        client.chat.completions.create.return_value = mock_response
        return client

    def test_parses_valid_response(self):
        client = self._make_client({
            "score": 8,
            "reasoning": "Strong AI focus",
            "estimated_salary": "130-150k EUR",
            "effort_flag": "sweet-spot",
            "prep_level": 2,
            "prep_notes": "Brush up on MLOps",
        })

        score, reasoning, salary, effort, prep, notes = score_job(
            client, "AI PM", "Mistral", "Build AI products"
        )

        assert score == 8
        assert reasoning == "Strong AI focus"
        assert salary == "130-150k EUR"
        assert effort == "sweet-spot"
        assert prep == 2
        assert notes == "Brush up on MLOps"

    def test_handles_missing_description(self):
        client = MagicMock()
        score, reasoning, salary, effort, prep, notes = score_job(
            client, "Test", "Co", None
        )
        assert score == 0
        assert "No description" in reasoning
        # Should not call OpenAI
        client.chat.completions.create.assert_not_called()

    def test_handles_nan_description(self):
        client = MagicMock()
        score, reasoning, salary, effort, prep, notes = score_job(
            client, "Test", "Co", float("nan")
        )
        assert score == 0

    def test_handles_json_parse_error(self):
        client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "not json at all"
        client.chat.completions.create.return_value = mock_response

        score, reasoning, salary, effort, prep, notes = score_job(
            client, "Test", "Co", "Some description"
        )

        assert score == 5  # default fallback
        assert "Parse error" in reasoning

    def test_handles_missing_optional_fields(self):
        client = self._make_client({
            "score": 6,
            "reasoning": "Okay fit",
        })

        score, reasoning, salary, effort, prep, notes = score_job(
            client, "PM", "Co", "Product work"
        )

        assert score == 6
        assert salary == "unknown"
        assert effort == "unknown"
        assert prep == 0
        assert notes == "unknown"

    def test_truncates_long_description(self):
        client = self._make_client({
            "score": 5,
            "reasoning": "Average",
            "estimated_salary": "unknown",
            "effort_flag": "unknown",
            "prep_level": 3,
            "prep_notes": "Study domain",
        })

        long_desc = "x" * 10000
        score_job(client, "Test", "Co", long_desc)

        # Check that the description passed to the API was truncated
        call_args = client.chat.completions.create.call_args
        user_msg = call_args[1]["messages"][1]["content"]
        # Original was 10000 chars, should be truncated to 3000
        assert len(long_desc) > 3000
        assert "x" * 3000 in user_msg

    def test_returns_correct_types(self):
        client = self._make_client({
            "score": "7",  # string instead of int
            "reasoning": "Good fit",
            "estimated_salary": "100k",
            "effort_flag": "moderate",
            "prep_level": "3",  # string instead of int
            "prep_notes": "Some prep",
        })

        score, reasoning, salary, effort, prep, notes = score_job(
            client, "Test", "Co", "Description"
        )

        assert isinstance(score, int)
        assert isinstance(prep, int)
        assert score == 7
        assert prep == 3
