# modeling/benchmark/sciencebench.py

import re
import uuid
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Tuple, Optional, Dict, TYPE_CHECKING
import pandas as pd
import logging
import sys

from modeling.benchmark.benchmark import BaseBenchmark
from modeling.utils.paths import get_benchmarks_dir

# Add benchmarks directory to sys.path so sciencebench can be imported directly
_BENCHMARKS_DIR = get_benchmarks_dir()
if str(_BENCHMARKS_DIR) not in sys.path:
    sys.path.insert(0, str(_BENCHMARKS_DIR))

# Import utils module to support dynamic imports
from benchmarks.mlebench import utils as mlebench_utils

# --- Modeling core model imports ---
from modeling.models.task import TaskDefinition

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from modeling.runner import ModelingRunner


METADATA_FIELDS = [
    "instance_id",
    "domain",
    "subtask_categories",
    "task_inst",
    "domain_knowledge",
    "dataset_folder_tree",
    "dataset_preview",
    "src_file_or_path",
    "github_name",
    "gold_program_name",
    "output_fname",
    "eval_script_name",
]


# Simple data class for competition reports
class CompetitionReport:
    """Simple competition report for grading results."""
    def __init__(self, competition_id: str, score: float, submission_path: str,
                 valid_submission: bool = True, error_message: str = None):
        self.competition_id = competition_id
        self.score = score
        self.submission_path = submission_path
        self.submission_exists = Path(submission_path).exists()
        self.valid_submission = valid_submission
        self.error_message = error_message
        self.gold_medal = False
        self.silver_medal = False
        self.bronze_medal = False
        self.above_median = False
        self.is_lower_better = False
        self.created_at = datetime.now().isoformat()


class ScienceBenchmark(BaseBenchmark):
    """
    Benchmark class for ScienceBench - 102 scientific computing tasks.

    Supports tasks from:
    - Computational Chemistry (20 tasks)
    - Geographical Information Science (27 tasks)
    - Bioinformatics (27 tasks)
    - Psychology and Cognitive Science (28 tasks)
    """

    def __init__(
        self,
        name: str,
        file_path: Optional[str],
        log_path: str,
        data_dir: Optional[str] = None,
        competitions: Optional[List[str]] = None
    ):
        """
        Initialize ScienceBench.

        Args:
            name: Benchmark name
            file_path: Path to config file (optional)
            log_path: Path to save logs
            data_dir: Path to data directory (competitions prepared data).
                     If not provided, will raise an error.
            competitions: List of specific competition IDs to run (optional)
        """
        # Validate data_dir is provided
        if data_dir is None:
            raise ValueError(
                "data_dir is required for ScienceBenchmark. "
                "Please provide --data-dir argument pointing to the competitions directory."
            )

        self.data_dir = Path(data_dir).resolve()
        self.registry_dir = get_benchmarks_dir("sciencebench") / "competitions"

        # Derive metadata path from data_dir
        # Assumes metadata is at: <data_dir>/../benchmark/ScienceAgentBench.csv
        metadata_path = self.data_dir.parent / "benchmark" / "ScienceAgentBench.csv"

        # Load config or create default
        self.config = self._load_config(file_path) if file_path else {}

        # Override with specific competitions if provided
        if competitions:
            self.config["competitions"] = list(competitions)

        self.metadata_index = self._load_metadata_index(metadata_path)

        super().__init__(name, file_path, log_path)

        # Create log directory
        Path(self.log_path).mkdir(parents=True, exist_ok=True)

        # Load problems
        self.problems = self._load_problems()

        logger.info(f"ScienceBenchmark initialized with data_dir: {self.data_dir}")
        logger.info(f"Registry directory: {self.registry_dir}")
        logger.info(f"Loaded {len(self.problems)} competition(s)")

    def _load_config(self, file_path: Optional[str]) -> Dict[str, Any]:
        """Load benchmark configuration from YAML file."""
        if not file_path:
            return {}

        config_path = Path(file_path)
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return {}

        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config or {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _load_metadata_index(self, metadata_path: Path) -> Dict[int, Dict[str, Any]]:
        """Load ScienceAgentBench metadata for task-specific contextual data."""
        if not metadata_path or not metadata_path.exists():
            logger.warning("ScienceBench metadata CSV not found: %s", metadata_path)
            return {}

        try:
            df = pd.read_csv(metadata_path)
        except Exception as exc:
            logger.warning("Failed to load ScienceBench metadata from %s: %s", metadata_path, exc)
            return {}

        metadata_index: Dict[int, Dict[str, Any]] = {}
        for _, row in df.iterrows():
            if "instance_id" not in row:
                continue
            try:
                instance_id = int(row["instance_id"])
            except (TypeError, ValueError):
                continue

            entry: Dict[str, Any] = {}
            for field in METADATA_FIELDS:
                if field not in row:
                    continue
                value = row[field]
                if pd.isna(value):
                    entry[field] = None
                else:
                    python_value = value.item() if hasattr(value, "item") else value
                    if isinstance(python_value, str):
                        python_value = python_value.strip()
                    entry[field] = python_value

            metadata_index[instance_id] = entry

        logger.info(
            "Loaded ScienceBench metadata for %d task(s) from %s",
            len(metadata_index),
            metadata_path,
        )
        return metadata_index

    def _load_problems(self) -> List[Dict[str, Any]]:
        """
        Load competition problems from the registry.

        Returns:
            List of problem dictionaries with competition metadata
        """
        logger.info(f"Discovering competitions in registry: {self.registry_dir}")

        problems = []

        # Get competition IDs from config or scan directory
        if "competitions" in self.config and self.config["competitions"]:
            competition_ids = self.config["competitions"]
        else:
            # Scan registry directory for all competitions
            competition_ids = []
            for item in self.registry_dir.iterdir():
                if item.is_dir() and item.name.startswith("sciencebench-"):
                    competition_ids.append(item.name)
            competition_ids.sort()

        logger.info(f"Found {len(competition_ids)} competition(s) in configuration/registry")

        # Iterate over competitions
        for competition_id in competition_ids:
            try:
                # Check if registry exists
                comp_registry_dir = self.registry_dir / competition_id
                config_file = comp_registry_dir / "config.yaml"

                if not config_file.exists():
                    logger.warning(f"Skipping '{competition_id}': config.yaml not found")
                    continue

                # Check if data is prepared
                comp_data_dir = self.data_dir / competition_id / "prepared"
                public_dir = comp_data_dir / "public"
                private_dir = comp_data_dir / "private"

                instance_id = self._extract_instance_id_from_competition_id(competition_id)
                metadata_entry = self.metadata_index.get(instance_id) if instance_id is not None else None

                # Add competition (data can be prepared on-demand)
                problems.append({
                    "competition_id": competition_id,
                    "registry_dir": str(comp_registry_dir),
                    "data_dir": str(comp_data_dir),
                    "instance_id": instance_id,
                    "metadata": metadata_entry.copy() if isinstance(metadata_entry, dict) else None,
                    "data_prepared": public_dir.exists() and private_dir.exists()
                })

                status = "prepared" if (public_dir.exists() and private_dir.exists()) else "not prepared"
                logger.debug(f"Loaded competition: {competition_id} ({status})")

            except Exception as e:
                logger.warning(f"Error loading competition '{competition_id}': {e}")

        if not problems:
            logger.warning(
                f"No competitions found. Registry: {self.registry_dir}, Data: {self.data_dir}"
            )

        return problems

    @staticmethod
    def _extract_instance_id_from_competition_id(competition_id: str) -> Optional[int]:
        """Extract numeric instance_id from a ScienceBench competition identifier."""
        match = re.search(r"sciencebench-(\d+)", competition_id or "")
        if not match:
            return None
        try:
            return int(match.group(1))
        except ValueError:
            return None

    def get_result_columns(self) -> List[str]:
        return [
            "competition_id", "submission_path", "answers_path", "score", "cost",
            "gold_medal", "silver_medal", "bronze_medal", "above_median",
            "submission_exists", "valid_submission", "error_message",
        ]

    def _load_dataframe(self, path: Path) -> pd.DataFrame:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".pkl", ".pickle"}:
            try:
                return pd.read_pickle(path)
            except ModuleNotFoundError as exc:
                if "numpy._core.numeric" in str(exc):
                    import numpy as np
                    import sys
                    import numpy.core.numeric  # ensure module is importable
                    sys.modules.setdefault("numpy._core", np.core)
                    sys.modules.setdefault("numpy._core.numeric", numpy.core.numeric)
                    return pd.read_pickle(path)
                raise
        if suffix == ".json":
            return pd.read_json(path)

        raise ValueError(f"Unsupported submission format: {path.suffix}")

    def _resolve_answers_path(self, problem: Dict[str, Any]) -> Optional[Path]:
        try:
            registry_dir = Path(problem["registry_dir"])
            with open(registry_dir / "config.yaml", "r", encoding="utf-8") as handle:
                config = yaml.safe_load(handle) or {}
            dataset_cfg = config.get("dataset") or {}
            answers_rel = dataset_cfg.get("answers")
            if not answers_rel:
                return None
            return self.data_dir / answers_rel
        except Exception as exc:
            logger.warning("Unable to resolve answers path: %s", exc)
            return None

    def _create_error_report(self, competition_id: str, submission_path: Path, error_msg: str) -> CompetitionReport:
        """Creates a dummy report if grading or eval_fn execution fails."""
        report = CompetitionReport(
            competition_id=competition_id,
            score=0.0,
            submission_path=str(submission_path),
            valid_submission=False,
            error_message=error_msg
        )
        logger.error(f"Error for {competition_id}: {error_msg}")
        return report

    async def evaluate_problem(
        self,
        problem: dict,
        eval_fn: Callable,
        runner: Optional["ModelingRunner"] = None
    ) -> Tuple[Tuple, CompetitionReport, Optional[str]]:
        """
        Evaluates a single ScienceBench competition.
        """
        competition_id = problem.get("competition_id")
        if not competition_id:
            raise ValueError("Problem data must contain 'competition_id'")

        # Define unique output path
        unique_id = uuid.uuid4().hex[:6]
        output_filename = f"submission_{competition_id}_{unique_id}.csv"
        output_submission_path = (Path(self.log_path) / output_filename).absolute()

        cost = 0.0
        report: Optional[CompetitionReport] = None
        error_message: Optional[str] = None

        try:
            # Load competition config
            registry_dir = Path(problem["registry_dir"])
            with open(registry_dir / "config.yaml", 'r') as f:
                config = yaml.safe_load(f)

            # Load description
            description_file = registry_dir / "description.md"
            if description_file.exists():
                with open(description_file, 'r') as f:
                    description = f.read()
            else:
                description = f"# {config.get('name', competition_id)}"

            metadata_payload: Dict[str, Any] = {}
            raw_metadata = problem.get("metadata")
            if isinstance(raw_metadata, dict):
                metadata_payload = {k: v for k, v in raw_metadata.items()}
            instance_id = problem.get("instance_id")
            if instance_id is not None:
                metadata_payload.setdefault("instance_id", instance_id)

            # Get public data directory
            public_dir = Path(problem["data_dir"]) / "public"

            # Check if dataset is prepared
            if not public_dir.exists():
                raise ValueError(f"Dataset for '{competition_id}' not prepared in '{self.data_dir}'.")

            # 1. Create standardized TaskDefinition
            task = TaskDefinition(
                task_id=competition_id,
                task_type="science",
                payload={
                    "description": description,
                    "public_data_dir": str(public_dir.absolute()),
                    "output_submission_path": str(output_submission_path.absolute()),
                    "config_path": str((registry_dir / "config.yaml").absolute()),
                    "metadata": metadata_payload,
                    "competition_id": competition_id,
                }
            )

            # 2. Call the generic evaluation function
            result, cost = await eval_fn(task)

            # 3. Process result and perform grading
            if isinstance(result, Path):
                logger.debug(f"Grading submission {result} for {competition_id}")
                report = await self._grade_submission(result, problem)
            elif isinstance(result, str) and result.startswith("[ERROR]"):
                error_message = f"Modeling workflow failed: {result}"
                logger.error(error_message)
                report = self._create_error_report(competition_id, output_submission_path, error_message)
            else:
                error_message = f"Unexpected result type from eval_fn: {type(result).__name__}"
                logger.error(error_message)
                report = self._create_error_report(competition_id, output_submission_path, error_message)

        except Exception as e:
            error_message = f"Error during ScienceBenchmark evaluation of {competition_id}: {e}"
            logger.error(error_message, exc_info=True)
            report = self._create_error_report(competition_id, output_submission_path, error_message)

        if report is None:
            final_error = error_message or "Unknown error: report is None"
            report = self._create_error_report(competition_id, output_submission_path, final_error)
            error_message = final_error

        answers_path = self._resolve_answers_path(problem)

        if not report.valid_submission:
            self.log_mismatch(
                problem=competition_id,
                expected_output=str(answers_path) if answers_path else "<unknown>",
                prediction=f"File: {output_submission_path}, Exists: {report.submission_exists}, Valid: {report.valid_submission}",
                extracted_output=report.score,
                extract_answer_code=error_message or "Grading function failed or file invalid/missing"
            )
            if not error_message:
                error_message = "Submission invalid or missing."

        csv_tuple = (
            report.competition_id, str(report.submission_path), str(answers_path),
            report.score, cost, report.gold_medal, report.silver_medal, report.bronze_medal,
            report.above_median, report.submission_exists, report.valid_submission, error_message,
        )

        if runner:
            try:
                runner.record_grade_report(
                    task_id=competition_id,
                    submission_path=str(report.submission_path),
                    report=report,
                    error_message=error_message
                )
            except Exception as exc:
                logger.warning(
                    "Failed to record grade telemetry for '%s': %s",
                    competition_id,
                    exc
                )

        return csv_tuple, report, error_message

    async def _grade_submission(self, submission_path: Path, problem: Dict[str, Any]) -> CompetitionReport:
        """
        Grade a submission using the competition's grading function.
        """
        competition_id = problem["competition_id"]
        registry_dir = Path(problem["registry_dir"])

        try:
            # Load config
            with open(registry_dir / "config.yaml", 'r') as f:
                config = yaml.safe_load(f)

            # Import grade function dynamically using mlebench's import_fn
            grade_fn_str = config['grader']['grade_fn']

            # Use mlebench's import_fn which handles hyphens in module names
            grade_fn = mlebench_utils.import_fn(grade_fn_str)

            # Load submission
            if not submission_path.exists():
                return CompetitionReport(
                    competition_id=competition_id,
                    score=0.0,
                    submission_path=str(submission_path),
                    valid_submission=False,
                    error_message="Submission file not found"
                )

            submission_df = self._load_dataframe(submission_path)

            # Load answers
            answers_rel_path = config['dataset']['answers']
            answers_path = self.data_dir / answers_rel_path

            if not answers_path.exists():
                return CompetitionReport(
                    competition_id=competition_id,
                    score=0.0,
                    submission_path=str(submission_path),
                    valid_submission=False,
                    error_message=f"Answers file not found: {answers_path}"
                )

            answers_df = self._load_dataframe(answers_path)

            # Grade
            score = grade_fn(submission_df, answers_df)

            logger.info(f"Graded {competition_id}: score={score}")

            return CompetitionReport(
                competition_id=competition_id,
                score=float(score),
                submission_path=str(submission_path),
                valid_submission=True,
                error_message=None
            )

        except Exception as e:
            logger.error(f"Grading failed for {competition_id}: {e}")
            import traceback
            traceback.print_exc()

            return CompetitionReport(
                competition_id=competition_id,
                score=0.0,
                submission_path=str(submission_path),
                valid_submission=False,
                error_message=str(e)
            )

    def get_problem_by_id(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific problem by its ID."""
        for problem in self.problems:
            if problem["competition_id"] == problem_id:
                return problem
        return None
