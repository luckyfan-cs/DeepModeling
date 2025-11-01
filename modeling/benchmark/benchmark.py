import asyncio
import json
from pathlib import Path
from typing import Any, Callable, List, Tuple, Optional, Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BaseBenchmark:
    """
    Abstract base class for all benchmark tests.
    """
    def __init__(self, name: str, file_path: Optional[str], log_path: str, **kwargs):
        self.name = name
        self.file_path = file_path
        self.log_path = log_path
        self.problems = self._load_problems()
        # self.results_path = Path(self.log_path) / f"{self.name}_results.csv"
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_path = Path(self.log_path) / f"{self.name}_results_{timestamp}.csv"
        self.mismatches_path = Path(self.log_path) / f"{self.name}_mismatches.log"

    def _load_problems(self) -> List[Dict[str, Any]]:
        """Load problems from jsonl file."""
        # MODIFICATION: Handle cases where file_path is not provided.
        if not self.file_path:
            logger.debug("No file_path provided. Subclass is expected to override _load_problems.")
            return []
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    def get_result_columns(self) -> List[str]:
        raise NotImplementedError

    async def evaluate_problem(self, problem: Dict, eval_fn: Callable, **kwargs) -> Tuple:
        raise NotImplementedError

    def log_mismatch(self, **kwargs):
        with open(self.mismatches_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(kwargs) + "\n")

    # REFACTORED: The main evaluation loop now accepts and passes down `eval_fn`.
    async def run_evaluation(self, eval_fn: Callable, **kwargs):
        """
        Run the entire benchmark evaluation.

        Args:
            eval_fn: The generic evaluation function provided by ModelingRunner.get_eval_function().
        """
        if not self.problems:
            logger.error(f"Evaluation for '{self.name}' aborted: No problems were loaded.")
            return
        
        logger.info(f"Starting evaluation for benchmark '{self.name}' with {len(self.problems)} problems.")
        
        results = []
        tasks = [self.evaluate_problem(problem, eval_fn=eval_fn, **kwargs) for problem in self.problems]
        
        # Use native asyncio for task completion
        for future in asyncio.as_completed(tasks):
            try:
                # evaluate_problem returns (csv_tuple, report, error_message)
                result_tuple, report, error_message = await future
                results.append(result_tuple)
            except Exception as e:
                logger.error(f"An unexpected error occurred in evaluate_problem: {e}", exc_info=True)

        # Save results to CSV
        df = pd.DataFrame(results, columns=self.get_result_columns())
        df.to_csv(self.results_path, index=False)
        logger.info(f"Evaluation complete. Results saved to {self.results_path}")