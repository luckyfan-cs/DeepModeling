# modeling/services/data_analyzer.py

import logging
import traceback
from pathlib import Path
import pandas as pd
from typing import Optional, List

from modeling.models.task import TaskType
from modeling.utils.context import truncate_output

logger = logging.getLogger(__name__)


def generate_file_tree(
    start_path: Path,
    max_depth: int = 5,
    max_files: int = 100,
    max_items_per_dir: int = 20,
    display_root_name: Optional[str] = None
) -> str:
    """
    Generates a textual representation of the file tree with intelligent truncation.

    This version prevents a single large directory from consuming the entire file limit,
    and it filters out common noise files.

    Args:
        start_path: The root directory to start the tree from.
        max_depth: The maximum depth to traverse into directories.
        max_files: The global limit for the total number of files to display.
        max_items_per_dir: The maximum number of items (files and dirs) to show per directory.
        display_root_name: An optional name to display for the root directory.
    """
    tree = []
    start_path = Path(start_path)
    if not start_path.exists():
        return f"Directory not found: {start_path}"


    base_name = display_root_name if display_root_name is not None else start_path.name
    file_count = 0
    global_limit_reached = False

    def _walk(path: Path, prefix: str, depth: int):
        nonlocal file_count, global_limit_reached
        
        if depth > max_depth or global_limit_reached:
            return

        try:
            # Filter out ignored files and sort for deterministic output
            contents = sorted([p for p in path.iterdir()])
        except OSError as e:
            logger.warning(f"Error reading directory {path}: {e}")
            tree.append(f"{prefix}└── [Error reading directory]")
            return

        # Per-directory truncation logic
        truncated_in_dir = False
        if len(contents) > max_items_per_dir:
            display_items = contents[:max_items_per_dir // 2]
            truncated_in_dir = True
        else:
            display_items = contents

        pointers = ['├── '] * (len(display_items) - 1) + ['└── ']
        # If we truncated this directory, the last visible item is not the true last item
        if truncated_in_dir:
            pointers[-1] = '├── '

        for pointer, sub_path in zip(pointers, display_items):
            if global_limit_reached:
                return

            if not sub_path.is_dir():
                # Check global file limit *before* adding the next file
                if file_count >= max_files:
                    global_limit_reached = True
                    return
                file_count += 1

            display_name = sub_path.name + ('/' if sub_path.is_dir() else '')
            tree.append(f"{prefix}{pointer}{display_name}")

            if sub_path.is_dir():
                extension = '│   ' if pointer == '├── ' else '    '
                _walk(sub_path, prefix=prefix + extension, depth=depth + 1)

        if truncated_in_dir:
            remaining_count = len(contents) - len(display_items)
            tree.append(f"{prefix}└── [... {remaining_count} more items truncated ...]")

    tree.append(f"{base_name}/")
    _walk(start_path, prefix="", depth=1)

    if global_limit_reached:
        tree.append(f"\n[... Truncated. Total file limit ({max_files}) reached ...]")

    return "\n".join(tree)


class DataAnalyzer:
    """
    A centralized service for analyzing input data directories and generating
    a comprehensive textual overview for the Agent.
    """
    def analyze(self, data_dir: Path, output_filename: str, task_type: Optional[TaskType] = None, optimization_context: bool = False) -> str:
        """
        Analyzes the data directory and returns a formatted overview string,
        including critical I/O instructions.
        """
        report = self.analyze_data(data_dir, task_type)
        report += self.generate_io_instructions(output_filename, optimization_context)
        return report

    def analyze_data(self, data_dir: Path, task_type: Optional[TaskType] = None) -> str:
        """
        Analyzes the data directory and returns ONLY the data report (structure, format, etc.).
        Does NOT include I/O instructions.
        """
        if not data_dir or not data_dir.exists() or not data_dir.is_dir():
            logger.error(f"Data directory issue during analysis: {data_dir}")
            return "Error: Input data directory not found, not provided, or is not a directory."

        report = "\n\n--- COMPREHENSIVE DATA REPORT ---\n\n"

        # 1. Analyze File Structure (Universal)
        report += self._analyze_structure(data_dir)

        report += self._analyze_data_schema(data_dir)

        # 3. Task-Specific Analysis
        if task_type in {"kaggle", "science"}:
            submission_analysis = self._analyze_kaggle_submission_format(data_dir)
            if submission_analysis:
                report += f"## Submission Format Requirements\n{submission_analysis}\n\n"
        
        # Remove the call to _generate_io_instructions from here
        return report

    def generate_io_instructions(self, output_filename: str, optimization_context: bool = False) -> str:
        """
        Generate standardized I/O instructions reflecting that CWD is the input directory.
        """
        input_instructions = (
            "1. **INPUT DATA:**\n"
            "   - All input files are located in the **current working directory** (./).\n"
            "   - Example: Use `pd.read_csv('train.csv')`."
        )

        if optimization_context:
            output_instructions = (
                "2. **OUTPUT FILE (Dynamic Workflow Context):**\n"
                "   - Your workflow's `solve` method receives an `output_path` argument.\n"
                "   - You MUST save your final submission file using the filename derived from this argument (e.g., `output_path.name`).\n"
                "   - The file must be saved in the current working directory (./).\n"
                "   - **Example Write (Conceptual):** `final_df.to_csv(output_path.name, index=False)`"
            )
        else:
            output_instructions = (
                f"2. **OUTPUT FILE:**\n"
                f"   - You MUST save your final submission file to the **current working directory** (./).\n"
                f"   - The required output filename is: `{output_filename}`\n"
                f"   - **Correct Example:** `submission_df.to_csv('{output_filename}', index=False)`"
            )

        return f"""
--- CRITICAL I/O REQUIREMENTS ---

You MUST follow these file system rules precisely. Failure to do so will cause a fatal error.

{input_instructions}

{output_instructions}

**IMPORTANT:** These path requirements are non-negotiable and must be followed exactly.
"""

    def _analyze_structure(self, data_dir: Path) -> str:
        """Generates the file tree representation."""
        try:
            tree_output = generate_file_tree(data_dir, display_root_name=".")
            tree_output = truncate_output(tree_output)
            return f"## Directory Structure (Current Working Directory)\n```text\n{tree_output}\n```\n\n"
        except Exception as e:
            logger.error(f"Failed to generate file tree for {data_dir}: {traceback.format_exc()}")
            return f"## Directory Structure\nError analyzing structure: {traceback.format_exc()}\n\n"

    def _analyze_kaggle_submission_format(self, data_dir: Path) -> str:
        """
        Analyzes the sample submission file for Kaggle tasks and extracts a
        prescriptive schema.
        """
        sample_submission_file = self._find_sample_submission(data_dir)

        if not sample_submission_file:
            return ""

        try:
            # Read the sample submission file to get format details
            sample_df = pd.read_csv(sample_submission_file)

            # Get the first few rows and data types
            head_info = sample_df.head().to_string(index=False)
            dtypes_info = sample_df.dtypes.to_string()
            
            required_columns = sample_df.columns.tolist()
            columns_instruction = f"""
**Required Submission Columns:**
Your submission file MUST contain the following columns in this exact order:
```
{required_columns}
```
This is a strict requirement for the submission to be graded correctly. The grading system uses the non-prediction columns (like 'Comment' or an 'id') to match your predictions against the ground truth.
"""

            return f"""
**CRITICAL:** Your final submission file MUST EXACTLY match the format of the sample submission file provided (`{sample_submission_file.name}`).
This includes the column names, column order, and data types. Failure to adhere to this format will result in a score of zero.

{columns_instruction}

**Format Details:**
*First 5 rows:*
```text
{head_info}
```

*Data types:*
```text
{dtypes_info}
```

"""
        except Exception as e:
            # Fallback if pandas fails
            logger.warning(f"Could not read sample submission file '{sample_submission_file}' for detailed analysis: {traceback.format_exc()}")
            return f"""
**CRITICAL:** Your final submission file MUST match the format of the sample submission file: `{sample_submission_file.name}`.
(Note: Automatic format analysis failed, please inspect the file manually).
"""

    def _find_sample_submission(self, data_dir: Path) -> Optional[Path]:
        """Helper to locate the sample submission file."""
        try:
            for file in data_dir.iterdir():
                file_name_lower = file.name.lower()
                if "sample" in file_name_lower and "submission" in file_name_lower and file_name_lower.endswith(".csv"):
                    return file
        except Exception as e:
            logger.warning(f"Could not scan data directory '{data_dir}': {traceback.format_exc()}")
        return None

    def _analyze_data_schema(self, data_dir: Path) -> str:
        """
        Analyzes the schema of potential training and testing files to provide a
        structured overview of columns, data types, missing values, and cardinality.
        This helps the agent make better decisions about preprocessing.
        """
        report_parts = []
        # Define supported extensions and keywords for more robust discovery
        SUPPORTED_EXTENSIONS = ('.csv', '.tsv', '.parquet')
        KEYWORDS = ('train', 'test')

        # Use rglob for recursive search and more flexible name matching
        all_files = [p for p in data_dir.rglob('*') if p.is_file()]
        
        files_to_analyze = sorted([
            p for p in all_files
            if p.suffix.lower() in SUPPORTED_EXTENSIONS
            and any(keyword in p.stem.lower() for keyword in KEYWORDS)
        ])

        if not files_to_analyze:
            return ""

        for file_path in files_to_analyze:
            try:
                # Dynamically choose the reader based on file extension
                ext = file_path.suffix.lower()
                if ext in ['.csv', '.tsv']:
                    # pd.read_csv can often handle both with default settings
                    df = pd.read_csv(file_path)
                elif ext == '.parquet':
                    # Note: This requires 'pyarrow' or 'fastparquet' to be installed
                    df = pd.read_parquet(file_path)
                else:
                    # Skip unsupported but matched files
                    continue

                report_parts.append(f"### Analysis of `{file_path.relative_to(data_dir)}`")

                # Create a summary DataFrame
                summary = pd.DataFrame({
                    'Data Type': df.dtypes,
                    'Missing (%)': (df.isnull().sum() * 100 / len(df)).round(2),
                    'Cardinality': df.nunique(),
                })
                
                sample_values = [col.dropna().head(2).tolist() for _, col in df.items()]
                summary['Sample Values'] = sample_values

                # Truncate sample values for readability
                summary['Sample Values'] = summary['Sample Values'].apply(
                    lambda x: str(x) if len(str(x)) < 40 else str(x)[:37] + '...'
                )

                report_parts.append(f"```text\n{summary.to_string()}\n```")
            except Exception as e:
                logger.warning(f"Could not analyze schema for {file_path.name}: {traceback.format_exc()}")
                report_parts.append(f"### Analysis of `{file_path.relative_to(data_dir)}`\nCould not be analyzed due to error: {e}")

        if not report_parts:
            return ""

        analysis = "## Data Schema Analysis\n" + "\n\n".join(report_parts) + "\n\n"
        return truncate_output(analysis)
