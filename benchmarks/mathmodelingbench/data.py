from pathlib import Path

import pandas as pd

from .registry import Competition
from .utils import get_logger, is_empty, load_yaml

logger = get_logger(__name__)


def get_leaderboard(competition: Competition) -> pd.DataFrame:
    if not competition.leaderboard.is_file():
        raise FileNotFoundError(f"Leaderboard not found at {competition.leaderboard}")
    return pd.read_csv(competition.leaderboard)


def is_dataset_prepared(competition: Competition, grading_only: bool = False) -> bool:
    public = competition.public_dir
    private = competition.private_dir

    if not grading_only:
        if not public.is_dir():
            logger.warning("Public directory does not exist for %s", competition.id)
            return False
        if is_empty(public):
            logger.warning("Public directory is empty for %s", competition.id)
            return False

    if not private.is_dir():
        logger.warning("Private directory does not exist for %s", competition.id)
        return False
    if is_empty(private):
        logger.warning("Private directory is empty for %s", competition.id)
        return False

    if not competition.answers.is_file():
        logger.warning("Answers file missing for %s", competition.id)
        return False

    if not grading_only and not competition.sample_submission.is_file():
        logger.warning("Sample submission missing for %s", competition.id)
        return False

    return True
