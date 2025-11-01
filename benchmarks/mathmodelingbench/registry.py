from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from appdirs import user_cache_dir

from .grade_helpers import Grader
from .utils import (
    get_logger,
    get_module_dir,
    get_repo_dir,
    import_fn,
    load_yaml,
)

logger = get_logger(__name__)

DEFAULT_DATA_DIR = (Path(user_cache_dir()) / "mathmodeling-bench" / "data").resolve()


@dataclass(frozen=True)
class Competition:
    id: str
    name: str
    description: str
    grader: Grader
    answers: Path
    gold_submission: Path
    sample_submission: Path
    competition_type: str
    prepare_fn: Callable[[Path, Path, Path], None]
    raw_dir: Path
    private_dir: Path
    public_dir: Path
    checksums: Path
    leaderboard: Path

    @staticmethod
    def from_dict(data: dict) -> "Competition":
        grader = Grader.from_dict(data["grader"])
        return Competition(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            grader=grader,
            answers=data["answers"],
            gold_submission=data["gold_submission"],
            sample_submission=data["sample_submission"],
            competition_type=data["competition_type"],
            prepare_fn=data["prepare_fn"],
            raw_dir=data["raw_dir"],
            public_dir=data["public_dir"],
            private_dir=data["private_dir"],
            checksums=data["checksums"],
            leaderboard=data["leaderboard"],
        )


class Registry:
    def __init__(self, data_dir: Path | None = None):
        self._data_dir = Path(data_dir).resolve() if data_dir else DEFAULT_DATA_DIR
        self.mode = "test"

    def set_mode(self, mode: str = "test") -> None:
        if mode not in {"test", "validation", "prepare"}:
            raise ValueError("Mode must be one of {'test', 'validation', 'prepare'}.")
        self.mode = mode

    def get_data_dir(self) -> Path:
        return self._data_dir

    def set_data_dir(self, new_data_dir: Path) -> "Registry":
        return Registry(new_data_dir)

    def get_competition(self, competition_id: str) -> Competition:
        competitions_dir = self.get_competitions_dir()
        config_path = competitions_dir / competition_id / "config.yaml"

        if not config_path.is_file():
            raise FileNotFoundError(f"Competition config not found: {config_path}")

        config = load_yaml(config_path)

        checksums_path = config_path.parent / "checksums.yaml"
        leaderboard_path = config_path.parent / "leaderboard.csv"

        # Load description from competition directory
        description_relative = config["description"]
        if description_relative.startswith("benchmarks/mathmodelingbench/competitions/"):
            # Path includes "benchmarks/" prefix, load from config directory
            description_path = config_path.parent / "description.md"
        elif description_relative.startswith("mathmodelingbench/competitions/"):
            # Legacy path format, load from config directory
            description_path = config_path.parent / "description.md"
        else:
            # Relative path from repo root
            repo_root = get_repo_dir().parent  # Go up one more level to reach DeepModeling/
            description_path = repo_root / description_relative
        description = description_path.read_text(encoding="utf-8")

        config_preparer = config["preparer"]
        config_answers = config["dataset"]["answers"]
        config_sample_submission = config["dataset"]["sample_submission"]
        public_folder = "public"
        private_folder = "private"

        if self.mode == "prepare":
            config_preparer = config_preparer.replace("prepare:", "prepare_val:")
        elif self.mode == "validation":
            config_preparer = config_preparer.replace("prepare:", "prepare_val:")
            config_answers = config_answers.replace("/private/", "/private_val/")
            config_sample_submission = config_sample_submission.replace("/public/", "/public_val/")
            public_folder = "public_val"
            private_folder = "private_val"

        prepare_fn = import_fn(config_preparer)

        answers = self.get_data_dir() / config_answers
        gold_submission = (
            self.get_data_dir() / config["dataset"].get("gold_submission", config_answers)
        )
        sample_submission = self.get_data_dir() / config_sample_submission

        raw_dir = self.get_data_dir() / competition_id / "raw"
        private_dir = self.get_data_dir() / competition_id / "prepared" / private_folder
        public_dir = self.get_data_dir() / competition_id / "prepared" / public_folder

        return Competition.from_dict(
            {
                **config,
                "description": description,
                "answers": answers,
                "gold_submission": gold_submission,
                "sample_submission": sample_submission,
                "prepare_fn": prepare_fn,
                "raw_dir": raw_dir,
                "private_dir": private_dir,
                "public_dir": public_dir,
                "checksums": checksums_path,
                "leaderboard": leaderboard_path,
            }
        )

    def get_competitions_dir(self) -> Path:
        # Always return the module's competitions directory for loading config.yaml
        # The data_dir is used separately for loading actual data files (raw/, prepared/)
        return get_module_dir() / "competitions"

    def list_competition_ids(self) -> list[str]:
        competition_configs = self.get_competitions_dir().rglob("config.yaml")
        return [f.parent.stem for f in sorted(competition_configs)]


registry = Registry()
