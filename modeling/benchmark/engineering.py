import uuid
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
import logging

from modeling.benchmark.benchmark import BaseBenchmark
from modeling.utils.paths import get_config_file

# --- engineeringbench imports ---
from benchmarks.engineeringbench.data import is_dataset_prepared
from benchmarks.engineeringbench.grade import aggregate_reports, grade_csv
from benchmarks.engineeringbench.grade_helpers import CompetitionReport
from benchmarks.engineeringbench.registry import Competition, Registry
from benchmarks.engineeringbench import registry as DEFAULT_REGISTRY

# --- Modeling core imports ---
from modeling.models.task import TaskDefinition

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from modeling.runner import ModelingRunner


class EngineeringBenchmark(BaseBenchmark):
    """
    Benchmark integration for engineeringbench competitions.
    Mirrors the behavior of MLEBenchmark but uses the engineeringbench registry.
    """

    def __init__(
        self,
        name: str,
        file_path: Optional[str],
        log_path: str,
        data_dir: Optional[str] = None,
        tasks: Optional[List[str]] = None
    ):
        raw_data_dir = Path(data_dir) if data_dir else DEFAULT_REGISTRY.get_data_dir()
        if raw_data_dir.is_dir() and (raw_data_dir / "competitions").is_dir():
            self.data_dir = raw_data_dir / "competitions"
        else:
            self.data_dir = raw_data_dir
        self.registry: Registry = DEFAULT_REGISTRY.set_data_dir(self.data_dir)

        self.config = self._load_config()
        if tasks:
            self.config["competitions"] = list(tasks)

        super().__init__(name, file_path, log_path)
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        self.problems = self._load_problems()
        logger.info("EngineeringBenchmark initialized with data_dir: %s", self.data_dir)

    def _load_config(self) -> Dict[str, Any]:
        try:
            config_path = get_config_file()

            if not config_path.exists():
                logger.warning("Config file not found at %s, using default configuration", config_path)
                return {"competitions": ["industry-0"]}

            with open(config_path, "r", encoding="utf-8") as f:
                raw_config = yaml.safe_load(f) or {}

            competitions = raw_config.get("engineering_competitions")
            if not competitions:
                logger.warning(
                    "No `engineering_competitions` configured; defaulting to ['industry-0']"
                )
                competitions = ["industry-0"]
            return {"competitions": competitions}
        except Exception as exc:
            logger.error("Error loading config file: %s, using default configuration", exc)
            return {"competitions": ["industry-0"]}

    def _load_problems(self) -> List[Dict[str, Any]]:
        logger.info("Discovering prepared competitions in %s...", self.data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"EngineeringBench data directory not found: {self.data_dir}. "
                "Please provide a valid path via --data-dir."
            )

        problems: List[Dict[str, Any]] = []
        competition_ids = self.config.get("competitions", [])
        if not competition_ids:
            logger.warning("No competitions configured for EngineeringBenchmark")
            return problems

        for competition_id in competition_ids:
            try:
                competition = self.registry.get_competition(competition_id)
                if is_dataset_prepared(competition, grading_only=False):
                    problems.append({"competition_id": competition_id})
                    logger.debug("Found prepared competition: %s", competition_id)
                else:
                    logger.warning(
                        "Skipping competition '%s' as its dataset is not fully prepared.", competition_id
                    )
            except Exception as exc:
                logger.warning("Error loading competition '%s': %s", competition_id, exc)

        if not problems:
            logger.error(
                "No prepared competitions found in %s. "
                "Please prepare the datasets under the specified data directory.",
                self.data_dir,
            )

        return problems

    def _create_error_report(
        self,
        competition_id: str,
        submission_path: Path,
        error_msg: str
    ) -> CompetitionReport:
        base_data = {
            "competition_id": competition_id,
            "score": None,
            "gold_threshold": float("nan"),
            "silver_threshold": float("nan"),
            "bronze_threshold": float("nan"),
            "median_threshold": float("nan"),
            "any_medal": False,
            "gold_medal": False,
            "silver_medal": False,
            "bronze_medal": False,
            "above_median": False,
            "submission_exists": submission_path.exists(),
            "valid_submission": False,
            "is_lower_better": False,
            "created_at": datetime.now().isoformat(),
            "submission_path": str(submission_path),
        }
        report = CompetitionReport.from_dict(base_data)
        logger.error("Error for %s: %s", competition_id, error_msg)
        return report

    async def evaluate_problem(
        self,
        problem: dict,
        eval_fn: Callable,
        runner: Optional["ModelingRunner"] = None
    ) -> Tuple[Tuple, CompetitionReport, Optional[str]]:
        competition_id = problem.get("competition_id")
        if not competition_id:
            raise ValueError("Problem data must contain 'competition_id'")

        unique_id = uuid.uuid4().hex[:6]
        output_filename = f"submission_{competition_id}_{unique_id}.csv"
        output_submission_path = (Path(self.log_path) / output_filename).absolute()

        cost = 0.0
        report: Optional[CompetitionReport] = None
        error_message: Optional[str] = None
        competition: Optional[Competition] = None

        try:
            competition = self.registry.get_competition(competition_id)
            if not is_dataset_prepared(competition, grading_only=False):
                raise ValueError(
                    f"Dataset for '{competition_id}' not prepared in '{self.data_dir}'."
                )

            task = TaskDefinition(
                task_id=competition_id,
                task_type="kaggle",
                payload={
                    "description": competition.description,
                    "public_data_dir": str(competition.public_dir.absolute()),
                    "output_submission_path": str(output_submission_path.absolute()),
                },
            )

            result, cost = await eval_fn(task)

            if isinstance(result, Path):
                logger.debug("Grading submission %s for %s", result, competition_id)
                report = grade_csv(result, competition)
            elif isinstance(result, str) and result.startswith("[ERROR]"):
                error_message = f"Modeling workflow failed: {result}"
                logger.error(error_message)
                report = self._create_error_report(competition_id, output_submission_path, error_message)
            else:
                error_message = f"Unexpected result type from eval_fn: {type(result).__name__}"
                logger.error(error_message)
                report = self._create_error_report(competition_id, output_submission_path, error_message)

        except Exception as exc:
            error_message = f"Error during EngineeringBenchmark evaluation of {competition_id}: {exc}"
            logger.error(error_message, exc_info=True)
            report = self._create_error_report(competition_id, output_submission_path, error_message)

        if report is None:
            final_error = error_message or "Unknown error: report is None"
            report = self._create_error_report(competition_id, output_submission_path, final_error)
            error_message = final_error

        if not report.valid_submission:
            answers_path_str = str(getattr(competition, "answers", "N/A")) if competition else "N/A"
            self.log_mismatch(
                problem=competition_id,
                expected_output=answers_path_str,
                prediction=(
                    f"File: {output_submission_path}, Exists: {report.submission_exists}, "
                    f"Valid: {report.valid_submission}"
                ),
                extracted_output=report.score,
                extract_answer_code=error_message or "Grading function failed or file invalid/missing",
            )
            if not error_message:
                error_message = "Submission invalid or missing."

        answers_path_str = str(getattr(competition, "answers", "N/A")) if competition else "N/A"
        csv_tuple = (
            report.competition_id,
            str(report.submission_path),
            answers_path_str,
            report.score,
            cost,
            report.gold_medal,
            report.silver_medal,
            report.bronze_medal,
            report.above_median,
            report.submission_exists,
            report.valid_submission,
            error_message,
        )
        if runner:
            try:
                runner.record_grade_report(
                    task_id=competition_id,
                    submission_path=str(report.submission_path),
                    report=report,
                    error_message=error_message,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to record grade telemetry for '%s': %s",
                    competition_id,
                    exc,
                )
        return csv_tuple, report, error_message

    def get_result_columns(self) -> List[str]:
        return [
            "competition_id",
            "submission_path",
            "answers_path",
            "score",
            "cost",
            "gold_medal",
            "silver_medal",
            "bronze_medal",
            "above_median",
            "submission_exists",
            "valid_submission",
            "error_message",
        ]

    async def run_evaluation(self, eval_fn: Callable, **kwargs):
        await super().run_evaluation(eval_fn=eval_fn, **kwargs)
