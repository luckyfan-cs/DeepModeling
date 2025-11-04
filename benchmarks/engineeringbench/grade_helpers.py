"""Helper classes related to grading for engineeringbench."""
import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import pandas as pd

from .utils import get_logger, import_fn

logger = get_logger(__name__)


class InvalidSubmissionError(Exception):
    """Raised when a submission violates competition constraints."""


class Grader:
    def __init__(self, name: str, grade_fn: str) -> None:
        self.name = name
        self.grade_fn = import_fn(grade_fn)
        assert isinstance(self.name, str), "Grader name must be a string."
        assert len(self.name) > 0, "Grader name cannot be empty."

    def is_lower_better(self, leaderboard: pd.DataFrame) -> bool:
        scores = leaderboard["score"]
        top_score = scores.iloc[0]
        bottom_score = scores.iloc[-1]
        return bool(top_score < bottom_score)

    @staticmethod
    def from_dict(data: dict) -> "Grader":
        return Grader(**data)

    def __call__(self, submission: pd.DataFrame, answers: Any) -> Optional[float]:
        try:
            score = self.grade_fn(submission, answers)
        except InvalidSubmissionError as exc:
            logger.warning("Invalid submission: %s", exc)
            return None
        except Exception as exc:
            try:
                fpath = inspect.getfile(self.grade_fn)
                line_number = inspect.getsourcelines(self.grade_fn)[1]
                fn_info = f"{fpath}:{line_number}"
            except TypeError:
                fn_info = str(self.grade_fn)
            logger.error("Unexpected error during grading: %s. Check %s", exc, fn_info)
            return None
        return round(float(score), 5)

    def rank_score(self, score: Optional[float], leaderboard: pd.DataFrame) -> dict:
        assert "score" in leaderboard.columns, "Leaderboard must have a `score` column."

        lower_is_better = self.is_lower_better(leaderboard)
        num_teams = len(leaderboard)
        scores = leaderboard["score"]

        def get_score_at_position(position: int) -> float:
            if position - 1 >= len(scores) or position < 1:
                raise IndexError("Position out of bounds in the leaderboard.")
            return float(scores.iloc[position - 1])

        def get_thresholds(teams: int) -> tuple[float, float, float, float]:
            if 1 <= teams < 100:
                gold_threshold = get_score_at_position(max(1, int(teams * 0.1)))
                silver_threshold = get_score_at_position(max(1, int(teams * 0.2)))
                bronze_threshold = get_score_at_position(max(1, int(teams * 0.4)))
            elif 100 <= teams < 250:
                gold_threshold = get_score_at_position(10)
                silver_threshold = get_score_at_position(max(1, int(teams * 0.2)))
                bronze_threshold = get_score_at_position(max(1, int(teams * 0.4)))
            elif 250 <= teams < 1000:
                gold_threshold = get_score_at_position(10 + int(teams * 0.002))
                silver_threshold = get_score_at_position(50)
                bronze_threshold = get_score_at_position(100)
            elif teams >= 1000:
                gold_threshold = get_score_at_position(10 + int(teams * 0.002))
                silver_threshold = get_score_at_position(max(1, int(teams * 0.05)))
                bronze_threshold = get_score_at_position(max(1, int(teams * 0.1)))
            else:
                raise ValueError("Number of teams in leaderboard must be greater than 0.")

            median_threshold = float(scores.median())
            return gold_threshold, silver_threshold, bronze_threshold, median_threshold

        gold_threshold, silver_threshold, bronze_threshold, median_threshold = get_thresholds(
            num_teams
        )

        if score is None:
            return {
                "gold_medal": False,
                "silver_medal": False,
                "bronze_medal": False,
                "above_median": False,
                "gold_threshold": gold_threshold,
                "silver_threshold": silver_threshold,
                "bronze_threshold": bronze_threshold,
                "median_threshold": median_threshold,
            }

        assert isinstance(
            score, (float, int)
        ), f"Expected `score` to be a `float` or `int` but got {type(score)}."

        gold_medal = score <= gold_threshold if lower_is_better else score >= gold_threshold
        silver_medal = not gold_medal and (
            score <= silver_threshold if lower_is_better else score >= silver_threshold
        )
        bronze_medal = (
            not gold_medal
            and not silver_medal
            and (score <= bronze_threshold if lower_is_better else score >= bronze_threshold)
        )
        above_median = score < median_threshold if lower_is_better else score > median_threshold

        return {
            "gold_medal": gold_medal,
            "silver_medal": silver_medal,
            "bronze_medal": bronze_medal,
            "above_median": above_median,
            "gold_threshold": gold_threshold,
            "silver_threshold": silver_threshold,
            "bronze_threshold": bronze_threshold,
            "median_threshold": median_threshold,
        }


@dataclass(frozen=True)
class CompetitionReport:
    competition_id: str
    score: Optional[float]
    gold_threshold: float
    silver_threshold: float
    bronze_threshold: float
    median_threshold: float
    any_medal: bool
    gold_medal: bool
    silver_medal: bool
    bronze_medal: bool
    above_median: bool
    submission_exists: bool
    valid_submission: bool
    is_lower_better: bool
    created_at: datetime
    submission_path: str

    def to_dict(self) -> dict:
        return {
            "competition_id": self.competition_id,
            "score": float(self.score) if self.score is not None else None,
            "gold_threshold": float(self.gold_threshold),
            "silver_threshold": float(self.silver_threshold),
            "bronze_threshold": float(self.bronze_threshold),
            "median_threshold": float(self.median_threshold),
            "any_medal": bool(self.any_medal),
            "gold_medal": bool(self.gold_medal),
            "silver_medal": bool(self.silver_medal),
            "bronze_medal": bool(self.bronze_medal),
            "above_median": bool(self.above_median),
            "submission_exists": bool(self.submission_exists),
            "valid_submission": bool(self.valid_submission),
            "is_lower_better": bool(self.is_lower_better),
            "created_at": self.created_at.isoformat(),
            "submission_path": self.submission_path,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CompetitionReport":
        copied = data.copy()
        typed_data = {
            "competition_id": copied["competition_id"],
            "score": float(copied["score"]) if copied["score"] is not None else None,
            "gold_threshold": float(copied["gold_threshold"]),
            "silver_threshold": float(copied["silver_threshold"]),
            "bronze_threshold": float(copied["bronze_threshold"]),
            "median_threshold": float(copied["median_threshold"]),
            "any_medal": bool(copied["any_medal"]),
            "gold_medal": bool(copied["gold_medal"]),
            "silver_medal": bool(copied["silver_medal"]),
            "bronze_medal": bool(copied["bronze_medal"]),
            "above_median": bool(copied["above_median"]),
            "submission_exists": bool(copied["submission_exists"]),
            "valid_submission": bool(copied["valid_submission"]),
            "is_lower_better": bool(copied["is_lower_better"]),
            "created_at": datetime.fromisoformat(copied["created_at"])
            if isinstance(copied["created_at"], str)
            else copied["created_at"],
            "submission_path": copied["submission_path"],
        }
        return cls(**typed_data)
