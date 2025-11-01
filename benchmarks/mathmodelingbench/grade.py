"""High-level grading functionality for mathmodelingbench competitions."""
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .data import get_leaderboard, is_dataset_prepared
from .grade_helpers import CompetitionReport
from .registry import Competition, Registry
from . import registry as DEFAULT_REGISTRY
from .utils import (
    get_logger,
    get_timestamp,
    load_answers,
    purple,
    read_csv,
    read_jsonl,
)

logger = get_logger(__name__)


def grade_jsonl(path_to_submissions: Path, output_dir: Path, registry: Registry = DEFAULT_REGISTRY):
    submissions = read_jsonl(path_to_submissions, skip_commented_out_lines=True)
    competition_reports: list[CompetitionReport] = []

    for submission in submissions:
        submission_path = Path(str(submission["submission_path"]))
        competition_id = submission["competition_id"]
        competition = registry.get_competition(competition_id)
        report = grade_csv(submission_path, competition)
        competition_reports.append(report)

    aggregated = aggregate_reports(competition_reports)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"{get_timestamp()}_grading_report.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2)
    logger.info(purple(f"Saved summary report to {save_path}"))


def grade_csv(path_to_submission: Path, competition: Competition) -> CompetitionReport:
    if not is_dataset_prepared(competition, grading_only=True):
        raise ValueError(
            f"Dataset for competition `{competition.id}` is not prepared. "
            "Please ensure the data directory is correct or run the prepare script."
        )

    score = None
    submission_exists = path_to_submission.is_file() and path_to_submission.suffix.lower() == ".csv"
    if submission_exists:
        submission_df = read_csv(path_to_submission)
        logger.info(purple(f"Load answers from {competition.answers}"))
        answers = load_answers(competition.answers)
        score = competition.grader(submission_df, answers)
    else:
        logger.warning(
            "Invalid submission file for competition %s: %s", competition.id, path_to_submission
        )

    valid_submission = score is not None
    leaderboard = get_leaderboard(competition)
    rank_info = competition.grader.rank_score(score, leaderboard)
    is_lower_better = competition.grader.is_lower_better(leaderboard)

    return CompetitionReport(
        competition_id=competition.id,
        score=score,
        gold_threshold=rank_info["gold_threshold"],
        silver_threshold=rank_info["silver_threshold"],
        bronze_threshold=rank_info["bronze_threshold"],
        median_threshold=rank_info["median_threshold"],
        any_medal=rank_info["gold_medal"] or rank_info["silver_medal"] or rank_info["bronze_medal"],
        gold_medal=rank_info["gold_medal"],
        silver_medal=rank_info["silver_medal"],
        bronze_medal=rank_info["bronze_medal"],
        above_median=rank_info["above_median"],
        submission_exists=submission_exists,
        valid_submission=valid_submission,
        is_lower_better=is_lower_better,
        created_at=datetime.now(),
        submission_path=str(path_to_submission),
    )


def aggregate_reports(competition_reports: Iterable[CompetitionReport]) -> dict:
    reports = list(competition_reports)
    total_gold = sum(report.gold_medal for report in reports)
    total_silver = sum(report.silver_medal for report in reports)
    total_bronze = sum(report.bronze_medal for report in reports)
    total_above_median = sum(report.above_median for report in reports)
    total_submissions = sum(report.submission_exists for report in reports)
    total_valid = sum(report.valid_submission for report in reports)

    return {
        "total_runs": int(len(reports)),
        "total_runs_with_submissions": int(total_submissions),
        "total_valid_submissions": int(total_valid),
        "total_medals": int(total_gold + total_silver + total_bronze),
        "total_gold_medals": int(total_gold),
        "total_silver_medals": int(total_silver),
        "total_bronze_medals": int(total_bronze),
        "total_above_median": int(total_above_median),
        "competition_reports": [report.to_dict() for report in reports],
    }
