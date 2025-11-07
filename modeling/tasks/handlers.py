from abc import ABC, abstractmethod
from pathlib import Path
import tempfile
import logging
from typing import Tuple, Any, Dict, Optional
import math
import yaml
from modeling.models.task import TaskDefinition
from modeling.services.data_analyzer import DataAnalyzer

logger = logging.getLogger(__name__)


class TaskHandler(ABC):
    """
    Base class for handlers that translate between logical TaskDefinition and physical file interfaces required by ModelingWorkflow.

    Each handler encapsulates preparation and parsing logic for specific task types (e.g., Kaggle, QA),
    allowing the workflow itself to remain task-agnostic.
    """
    def __init__(self):
        """
        Initialize the handler and create a temporary, self-managed directory
        for storing physical files generated for the task.
        """
        try:
            self.temp_dir = tempfile.TemporaryDirectory()
        except Exception as e:
            logger.error(f"Failed to create temporary directory for TaskHandler: {e}")
            self.temp_dir = None

        self.analyzer = DataAnalyzer()

    @abstractmethod
    def prepare_input(self, task: TaskDefinition) -> Tuple[str, str, Path, Path]:
        """
        Prepare the physical file input required by the workflow.

        This method converts logical tasks into physical parameters needed by ModelingWorkflow.solve().

        Args:
            task: Logical task definition.

        Returns:
            A tuple (description, io_instructions, data_dir, output_path) to pass to workflow.solve().
        """
        raise NotImplementedError

    @abstractmethod
    def parse_output(self, output_path: Path) -> Any:
        """
        Parse the workflow's output file into structured results required by benchmarking.

        This method converts physical output files back into logical answers.

        Args:
            output_path: Path where the workflow saved its output.

        Returns:
            Final answer in the format expected by benchmarking (e.g., string for QA, Path object for Kaggle).
        """
        raise NotImplementedError

    def cleanup(self):
        """
        Explicitly clean up the temporary directory.
        """
        if self.temp_dir:
            try:
                self.temp_dir.cleanup()
                logger.debug(f"Successfully cleaned up temporary directory for {self.__class__.__name__}.")
            except Exception as e:
                logger.error(f"Error cleaning up temporary directory for {self.__class__.__name__}: {e}")

    def __del__(self):
        """Ensure cleanup is called when the object is garbage collected."""
        self.cleanup()


class KaggleTaskHandler(TaskHandler):
    """
    Handler for Kaggle-style file input/file output tasks.
    This is a "pass-through" implementation since tasks are already file-based.
    """
    def prepare_input(self, task: TaskDefinition) -> Tuple[str, str, Path, Path]:
        """Extract paths, analyze data, and separate description from I/O instructions."""
        if task.task_type != "kaggle":
            raise ValueError("KaggleTaskHandler can only handle tasks of type 'kaggle'.")

        description = task.payload.get("description")
        data_dir = Path(task.payload.get("public_data_dir"))
        output_path = Path(task.payload.get("output_submission_path"))

        if not all([description, data_dir, output_path]):
            raise ValueError("Kaggle task payload is missing required keys: 'description', 'public_data_dir', 'output_submission_path'.")
        if not data_dir.exists() or not data_dir.is_dir():
            raise FileNotFoundError(f"Kaggle public_data_dir not found: {data_dir}")

        logger.info(f"Analyzing input data for task '{task.task_id}'...")

        data_report = self.analyzer.analyze_data(data_dir, task_type="kaggle")
        io_instructions = self.analyzer.generate_io_instructions(output_path.name, optimization_context=False)

        augmented_description = f"{description}\n{data_report}"

        logger.debug(f"Preparing Kaggle task '{task.task_id}': data_dir='{data_dir}', output_path='{output_path}'")
        return augmented_description, io_instructions, data_dir, output_path

    def parse_output(self, output_path: Path) -> Path:
        """
        For Kaggle tasks, the result is the output file itself.
        This just validates that the file was created.
        """
        if not output_path.exists():
            # In actual evaluation, this will be caught and reported as a failure.
            logger.warning(f"Agent did not produce the required submission file at: {output_path}")
            # Return the path even if it doesn't exist, let the caller (e.g., benchmark) handle the file not found case.
        return output_path


class QATaskHandler(TaskHandler):
    """
    Handler for simple question-answer (QA) tasks.
    This is a "translation" implementation that converts string questions to files and expects answers as files.
    """
    def prepare_input(self, task: TaskDefinition) -> Tuple[str, str, Path, Path]:
        """Convert QA question to physical file input."""
        if task.task_type != "qa":
            raise ValueError("QATaskHandler can only handle tasks of type 'qa'.")
        if not self.temp_dir:
            raise RuntimeError("Temporary directory not available for QATaskHandler.")

        question = task.payload.get("question")
        if not question:
            raise ValueError("QA task payload is missing required key: 'question'.")

        data_dir = Path(self.temp_dir.name)

        # Create physical task representation
        problem_file = data_dir / "problem.txt"
        problem_file.write_text(question, encoding='utf-8')

        # Define output contract
        output_path = data_dir / "answer.txt"

        # This core instruction is now simpler
        core_instruction = (
            "Your task is to answer the question found in `problem.txt`. "
            "Write ONLY the final answer into the required output file."
        )

        data_report = self.analyzer.analyze_data(data_dir, task_type="qa")
        io_instructions = self.analyzer.generate_io_instructions(output_path.name, optimization_context=False)

        description = f"{core_instruction}\n{data_report}"

        logger.debug(f"Preparing QA task '{task.task_id}': input file='{problem_file}', expected output='{output_path}'")
        return description, io_instructions, data_dir, output_path

    def parse_output(self, output_path: Path) -> str:
        """Read and return the final answer string from the output file."""
        if not output_path.exists() or not output_path.is_file():
            logger.warning(f"Agent did not produce the answer file for QA task at: {output_path}")
            return "[ERROR] Agent did not produce an answer file."

        try:
            answer = output_path.read_text(encoding='utf-8').strip()
            logger.debug(f"Parsed QA answer from '{output_path}': '{answer[:50]}...'")
            return answer
        except Exception as e:
            logger.error(f"Failed to read or parse QA answer file '{output_path}': {e}")
            return f"[ERROR] Failed to parse answer file: {e}"


class ScienceTaskHandler(TaskHandler):
    """
    Handler for ScienceBench tasks with diverse output formats.

    The ScienceBench conversion preserves the benchmark's notion of the target
    artifact (e.g., a PNG visualization) while often requiring the participant
    to submit a structured file (typically a CSV mirroring the sample
    submission). This handler inspects the competition config and metadata to
    provide the agent with precise I/O guidance.
    """

    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff'}
    ARRAY_EXTENSIONS = {'.npy', '.npz'}
    SAMPLE_FILE_PATTERNS = ("sample_submission.*", "submission.*")
    OUTPUT_TYPE_DESCRIPTIONS = {
        '.csv': 'CSV file with predictions or structured results',
        '.png': 'Image artifact (PNG)',
        '.jpg': 'Image artifact (JPEG)',
        '.jpeg': 'Image artifact (JPEG)',
        '.tif': 'Image artifact (TIFF)',
        '.tiff': 'Image artifact (TIFF)',
        '.json': 'JSON document',
        '.npy': 'NumPy array file (.npy)',
        '.npz': 'Compressed NumPy arrays (.npz)',
        '.txt': 'Plain text file',
        '.pkl': 'Serialized pickle object',
        '.h5': 'HDF5 file',
    }

    def prepare_input(self, task: TaskDefinition) -> Tuple[str, str, Path, Path]:
        """
        Extract paths, analyze data, and generate output-format-specific I/O instructions.
        """
        if task.task_type != "science":
            raise ValueError("ScienceTaskHandler can only handle tasks of type 'science'.")

        payload = task.payload or {}
        description = payload.get("description")
        data_dir_raw = payload.get("public_data_dir")
        output_path_raw = payload.get("output_submission_path")
        metadata = payload.get("metadata") or {}
        config_path_raw = payload.get("config_path")
        competition_id = payload.get("competition_id")

        if not all([description, data_dir_raw, output_path_raw]):
            raise ValueError(
                "Science task payload is missing required keys: "
                "'description', 'public_data_dir', 'output_submission_path'."
            )

        data_dir = Path(data_dir_raw)
        output_path = Path(output_path_raw)
        config_path = Path(config_path_raw) if config_path_raw else None

        if not data_dir.exists() or not data_dir.is_dir():
            raise FileNotFoundError(f"Science public_data_dir not found: {data_dir}")

        logger.info("Analyzing input data for science task '%s'...", task.task_id)

        sample_submission = self._find_sample_submission_file(data_dir)
        config_requirements = self._load_config_requirements(config_path)
        output_info = self._detect_output_characteristics(output_path, metadata, sample_submission)

        original_name = output_info.get("original_name")
        if output_path.suffix.lower() == ".csv" and output_info.get("logical_extension") == ".pkl":
            output_path = output_path.with_suffix(".pkl")

        output_info["submission_extension"] = output_path.suffix.lower()

        data_report = self.analyzer.analyze_data(data_dir, task_type="science")

        augmented_description = "\n\n".join(part for part in [description.strip(), data_report] if part)

        io_instructions = self._generate_science_io_instructions(
            output_path=output_path,
            sample_submission=sample_submission,
            output_info=output_info,
            config_requirements=config_requirements
        )

        logger.debug(
            "Preparing Science task '%s': data_dir='%s', output_path='%s', sample_submission='%s'",
            task.task_id,
            data_dir,
            output_path,
            sample_submission,
        )
        logger.debug("Science task output info: %s", output_info)

        return augmented_description, io_instructions, data_dir, output_path

    def parse_output(self, output_path: Path) -> Path:
        """
        For Science tasks, the result is the output file itself. We log the outcome
        and return the path for downstream grading.
        """
        if not output_path.exists():
            logger.warning("Agent did not produce the required science submission at: %s", output_path)
        else:
            file_size = output_path.stat().st_size
            logger.info("Science submission created: %s (%.1f KB)", output_path, file_size / 1024.0)
        return output_path

    def _generate_science_io_instructions(
        self,
        output_path: Path,
        sample_submission: Optional[Path],
        output_info: Dict[str, Any],
        config_requirements: Dict[str, Any]
    ) -> str:
        """
        Generate I/O instructions tailored to the detected submission format.
        """
        base_instructions = self.analyzer.generate_io_instructions(
            output_path.name,
            optimization_context=False,
        )

        submission_ext = output_info.get("submission_extension") or output_path.suffix.lower()
        expects_base64_csv = output_info.get("expects_base64_csv", False)
        logical_ext = output_info.get("logical_extension")

        notes: list[str] = []

        if expects_base64_csv:
            notes.append("- Encode generated images to base64 strings in the `image_base64` column.")

        if submission_ext == ".json":
            notes.append("- Produce valid JSON syntax (double quotes, no trailing commas).")

        if submission_ext in self.ARRAY_EXTENSIONS:
            notes.append("- Use NumPy save helpers (`numpy.save` / `numpy.savez`).")

        if submission_ext == ".txt":
            notes.append("- Write plain UTF-8 text without extra metadata.")

        if logical_ext in self.IMAGE_EXTENSIONS and not expects_base64_csv:
            notes.append("- Save a real image file (no base64) using the requested filename.")

        if submission_ext not in {".csv", ".json", ".txt"} and logical_ext not in (self.ARRAY_EXTENSIONS | self.IMAGE_EXTENSIONS):
            notes.append("- Ensure the output can be opened with standard Python tooling for that format.")

        if not notes:
            if submission_ext == '.pkl':
                base_instructions = base_instructions.replace('.to_csv(', '.to_pickle(')
                base_instructions = base_instructions.replace(', index=False', '')
            return base_instructions

        if submission_ext == '.pkl':
            base_instructions = base_instructions.replace('.to_csv(', '.to_pickle(')
            base_instructions = base_instructions.replace(', index=False', '')

        return f"{base_instructions}\n\n" + "\n".join(notes)

    def _find_sample_submission_file(self, data_dir: Path) -> Optional[Path]:
        """Locate the sample submission file within the public data directory."""
        if not data_dir.exists():
            return None

        for pattern in self.SAMPLE_FILE_PATTERNS:
            for candidate in sorted(data_dir.glob(pattern)):
                if candidate.is_file():
                    return candidate
        return None

    def _load_config_requirements(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Extract useful requirement hints from competition config.yaml."""
        if not config_path or not config_path.exists():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as handle:
                config_data = yaml.safe_load(handle) or {}
        except Exception as exc:
            logger.warning("Failed to read ScienceBench config at '%s': %s", config_path, exc)
            return {}

        grader = config_data.get("grader") or {}
        dataset_cfg = config_data.get("dataset") or {}

        requirements: Dict[str, Any] = {}
        grader_name = grader.get("name")
        if grader_name:
            requirements["grader_name"] = grader_name

        competition_type = config_data.get("competition_type")
        if competition_type:
            requirements["competition_type"] = competition_type

        sample_rel = dataset_cfg.get("sample_submission")
        if sample_rel:
            requirements["sample_submission_relpath"] = sample_rel

        return requirements

    def _format_metadata_summary(
        self,
        metadata: Dict[str, Any],
        output_info: Dict[str, Any],
        config_requirements: Dict[str, Any],
        competition_id: Optional[str]
    ) -> str:
        """Build a short contextual summary from ScienceBench metadata."""
        metadata = metadata if isinstance(metadata, dict) else {}

        lines = []
        if competition_id:
            lines.append(f"- Competition ID: {competition_id}")

        domain = self._normalize_value(metadata.get("domain"))
        if domain:
            lines.append(f"- Domain: {domain}")

        categories = self._normalize_value(metadata.get("subtask_categories"))
        if categories:
            lines.append(f"- Subtask Categories: {categories}")

        benchmark_hint = self._normalize_value(metadata.get("task_inst"))
        if benchmark_hint:
            preview = benchmark_hint if len(benchmark_hint) <= 400 else benchmark_hint[:397].rstrip() + "..."
            lines.append(f"- Benchmark Instruction Hint: {preview}")

        domain_knowledge = self._normalize_value(metadata.get("domain_knowledge"))
        if domain_knowledge:
            knowledge_preview = domain_knowledge if len(domain_knowledge) <= 300 else domain_knowledge[:297].rstrip() + "..."
            lines.append(f"- Domain Knowledge Notes: {knowledge_preview}")

        source_ref = self._normalize_value(metadata.get("src_file_or_path"))
        if source_ref:
            lines.append(f"- Source Reference: {source_ref}")

        original_name = output_info.get("original_name")
        if original_name:
            lines.append(f"- Original Benchmark Output: {original_name}")

        competition_type = config_requirements.get("competition_type")
        if competition_type:
            lines.append(f"- Competition Type: {competition_type}")

        if not lines:
            return ""

        header = "--- SCIENCE TASK CONTEXT ---"
        return "\n".join([header, *lines])

    def _detect_output_characteristics(
        self,
        output_path: Path,
        metadata: Dict[str, Any],
        sample_submission: Optional[Path]
    ) -> Dict[str, Any]:
        """Infer logical and physical output formats for the task."""
        metadata = metadata if isinstance(metadata, dict) else {}
        original_name_value = self._normalize_value(metadata.get("output_fname"))

        logical_ext = Path(original_name_value).suffix.lower() if original_name_value else ""
        submission_ext = sample_submission.suffix.lower() if sample_submission else output_path.suffix.lower()

        if not logical_ext:
            logical_ext = output_path.suffix.lower()

        is_image = logical_ext in self.IMAGE_EXTENSIONS
        expects_base64_csv = is_image and submission_ext == ".csv"

        output_type_desc = self.OUTPUT_TYPE_DESCRIPTIONS.get(
            logical_ext,
            f"{logical_ext} file" if logical_ext else "file"
        )
        submission_type_desc = self.OUTPUT_TYPE_DESCRIPTIONS.get(
            submission_ext,
            f"{submission_ext} file" if submission_ext else "file"
        )

        return {
            "original_name": original_name_value,
            "logical_extension": logical_ext,
            "submission_extension": submission_ext,
            "is_image": is_image,
            "expects_base64_csv": expects_base64_csv,
            "output_type_desc": output_type_desc,
            "submission_type_desc": submission_type_desc,
        }

    @staticmethod
    def _normalize_value(value: Any) -> Optional[Any]:
        """Normalize metadata values by stripping whitespace and dropping NaNs."""
        if value is None:
            return None
        try:
            # Handle pandas/numpy scalar NaNs
            if isinstance(value, float) and math.isnan(value):
                return None
        except TypeError:
            pass

        if hasattr(value, "item"):
            try:
                value = value.item()
            except Exception:
                pass

        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value
