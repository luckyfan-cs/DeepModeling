# main.py

import argparse
import asyncio
import inspect
import logging
import multiprocessing
import os
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from rich.console import Console, Group
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

# --- Modeling Core Component Imports ---
from modeling.config import ModelingConfig, LLMConfig, WorkflowConfig
from modeling.runner import ModelingRunner, WORKFLOW_FACTORIES

# --- Benchmark Class Imports ---
from modeling.benchmark.benchmark import BaseBenchmark
from modeling.benchmark.mle import MLEBenchmark
from modeling.benchmark.mathmodeling import MathModelingBenchmark
# from benchmarks.humaneval import HumanEvalBenchmark # Future additions can be easily added

# load .env file
load_dotenv()

# --- Logging Setup ---
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
)
logger = logging.getLogger(__name__)


# Benchmark Registry
BENCHMARK_CLASSES = {
    "mle": MLEBenchmark,
    "mathmodeling": MathModelingBenchmark,
    # "humaneval": HumanEvalBenchmark,
}


def _get_env_setting(name: str, default=None):
    """Read an env var and strip quotes/whitespace."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().strip('"').strip("'")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Modeling: A general-purpose agent evaluation framework.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--workflow",
        type=str,
        required=True,
        choices=WORKFLOW_FACTORIES.keys(),
        help="Agent workflow to run."
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        required=True,
        choices=BENCHMARK_CLASSES.keys(),
        help="Benchmark to execute."
    )
    parser.add_argument(
        "--dataset-file",
        type=str,
        required=False,
        default=None,
        help="Benchmark .jsonl path (optional, not used by MLE)."
    )
    parser.add_argument(
        "--log-path",
        type=str,
        default="runs/benchmark_results",
        help="Directory for logs and artifacts."
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Optional data directory for the selected benchmark/task."
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default=None,
        help="Override default LLM model."
    )
    parser.add_argument(
        "--llm-provider",
        type=str,
        default=None,
        help="Override LiteLLM provider alias (e.g. 'siliconflow')."
    )
    parser.add_argument(
        "--task",
        type=str,
        nargs="+",
        default=None,
        help="Target task identifier(s) for the selected benchmark."
    )
    return parser.parse_args()


def _build_benchmark_summary(results_path: Optional[Path], run_records: List[Dict[str, Any]]):
    """
    Build a summary table from the CSV results and the runner's metadata records.
    """
    df = None
    if results_path and Path(results_path).exists():
        try:
            df = pd.read_csv(results_path)
        except Exception as exc:
            logger.warning("Failed to load benchmark results from %s: %s", results_path, exc)

    records_by_task = {record.get("task_id"): record for record in run_records if record.get("task_id")}
    table = Table(
        title="[bold]Per-Competition Results[/bold]",
        show_lines=True,
        expand=True,
    )
    table.add_column("Competition", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right")
    table.add_column("Cost ($)", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Duration", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Metadata", style="green")

    totals = {
        "count": 0,
        "success": 0,
        "cost": 0.0,
        "tokens": 0,
        "duration": 0.0,
        "score": 0.0,
        "score_count": 0,
    }
    rows_added = False
    seen_record_keys = set()
    cwd = Path.cwd()

    def is_nan(value: Any) -> bool:
        try:
            return math.isnan(float(value))
        except (TypeError, ValueError):
            return False

    def format_score(value: Any) -> str:
        if value is None or is_nan(value):
            return "—"
        try:
            return f"{float(value):.4f}"
        except (TypeError, ValueError):
            return "—"

    def format_cost(value: Any) -> str:
        if value is None or is_nan(value):
            return "—"
        try:
            return f"${float(value):.2f}"
        except (TypeError, ValueError):
            return "—"

    def format_tokens(value: Any) -> str:
        if value is None or is_nan(value):
            return "—"
        try:
            return f"{int(value):,}"
        except (TypeError, ValueError):
            return "—"

    def format_duration(value: Any) -> str:
        if value is None or is_nan(value):
            return "—"
        try:
            return f"{float(value):.1f}s"
        except (TypeError, ValueError):
            return "—"

    def add_row(competition_id: str, score_val: Any, cost_val: Any, record: Optional[Dict[str, Any]]):
        nonlocal rows_added
        display_cost_val = cost_val
        if (display_cost_val is None or is_nan(display_cost_val)) and record:
            display_cost_val = record.get("summary", {}).get("total_cost")

        tokens_val = record.get("summary", {}).get("usage", {}).get("total_tokens") if record else None
        duration_val = record.get("timeline", {}).get("duration_seconds") if record else None
        success_flag = record.get("summary", {}).get("success") if record else None
        if success_flag is True:
            result_label = "✅ success"
        elif success_flag is False:
            result_label = "❌ failure"
        else:
            result_label = "—"

        metadata_path = record.get("metadata_path") if record else None
        if metadata_path:
            try:
                metadata_display = os.path.relpath(metadata_path, cwd)
            except Exception:
                metadata_display = metadata_path
        else:
            metadata_display = "—"

        table.add_row(
            competition_id or "N/A",
            format_score(score_val),
            format_cost(display_cost_val),
            format_tokens(tokens_val),
            format_duration(duration_val),
            result_label,
            metadata_display,
        )
        rows_added = True

        totals["count"] += 1
        if success_flag:
            totals["success"] += 1

        if display_cost_val is not None and not is_nan(display_cost_val):
            try:
                totals["cost"] += float(display_cost_val)
            except (TypeError, ValueError):
                pass

        if record:
            record_key = record.get("metadata_path") or record.get("task_id")
            if record_key:
                seen_record_keys.add(record_key)
            if tokens_val is not None and not is_nan(tokens_val):
                try:
                    totals["tokens"] += int(tokens_val)
                except (TypeError, ValueError):
                    pass
            if duration_val is not None and not is_nan(duration_val):
                try:
                    totals["duration"] += float(duration_val)
                except (TypeError, ValueError):
                    pass

        if score_val is not None and not is_nan(score_val):
            try:
                totals["score"] += float(score_val)
                totals["score_count"] += 1
            except (TypeError, ValueError):
                pass

    if df is not None and "competition_id" in df.columns:
        for _, row in df.iterrows():
            comp_id = str(row.get("competition_id", "")).strip() or "N/A"
            score_val = row.get("score")
            cost_val = row.get("cost")
            record = records_by_task.get(comp_id)
            add_row(comp_id, score_val, cost_val, record)

    for record in run_records:
        record_key = record.get("metadata_path") or record.get("task_id")
        if record_key in seen_record_keys:
            continue
        add_row(record.get("task_id", "N/A"), None, record.get("summary", {}).get("total_cost"), record)

    totals_table = None
    if rows_added:
        totals_table = Table.grid(padding=(0, 1))
        totals_table.add_column(style="bold cyan", justify="right")
        totals_table.add_column(justify="left")
        totals_table.add_row("Total tasks", str(totals["count"]))
        totals_table.add_row("Successful", str(totals["success"]))
        if totals["score_count"]:
            avg_score = totals["score"] / totals["score_count"]
            totals_table.add_row("Average score", format_score(avg_score))
        totals_table.add_row("Total cost", format_cost(totals["cost"]))
        totals_table.add_row("Total tokens", format_tokens(totals["tokens"]))
        totals_table.add_row("Total duration", format_duration(totals["duration"]))

    return (table if rows_added else None, totals_table)


async def main():
    """Main execution function."""
    args = parse_arguments()

    llm_model = args.llm_model or _get_env_setting("LLM_MODEL", "gpt-4o-mini")
    llm_provider = args.llm_provider or _get_env_setting("LLM_PROVIDER")
    llm_temperature = float(_get_env_setting("LLM_TEMPERATURE", "0.7"))
    api_key = _get_env_setting("API_KEY", "EMPTY")
    api_base = _get_env_setting("API_BASE", "https://api.openai.com/v1")

    # --- 1. Create Modeling Agent Configuration ---
    try:
        config = ModelingConfig(
            llm=LLMConfig(
                model=llm_model,
                temperature=llm_temperature,
                api_key=api_key,
                api_base=api_base,
                provider=llm_provider
            )
        )
        config.workflow = WorkflowConfig(name=args.workflow)
        config.run.keep_all_workspaces = True
        config.run.keep_workspace_on_failure = True
        config.run.parameters = {
            "workflow": args.workflow,
            "benchmark": args.benchmark,
            "dataset_file": args.dataset_file,
            "log_path": args.log_path,
            "data_dir": args.data_dir,
            "task": args.task,
            "llm_model": llm_model,
            "llm_provider": llm_provider,
            "llm_temperature": llm_temperature,
            "api_base": api_base,
        }
    except Exception as e:
        logger.error(f"Failed to create default ModelingConfig: {e}", exc_info=True)
        return

    run_name = f"{args.workflow}_on_{args.benchmark}"
    console.print(Panel(f"[bold]Agent Workflow:[/bold] {args.workflow}\n[bold]Benchmark:[/bold] {args.benchmark}", title="[bold cyan]Modeling Benchmark Run[/bold cyan]"))

    # --- 2. Instantiate Modeling Runner ---
    runner = ModelingRunner(config)

    # --- 3. Prepare benchmark ---
    benchmark_class = BENCHMARK_CLASSES.get(args.benchmark)
    if not benchmark_class:
        logger.error(f"Benchmark '{args.benchmark}' not found in registry.")
        return

    log_dir = Path(args.log_path) / run_name
    log_dir.mkdir(parents=True, exist_ok=True)

    benchmark_kwargs = {
        "name": args.benchmark,
        "file_path": args.dataset_file,
        "log_path": str(log_dir),
    }
    optional_params = {}
    if args.data_dir:
        optional_params["data_dir"] = args.data_dir
    if args.task:
        optional_params["tasks"] = args.task

    benchmark_init_params = set(inspect.signature(benchmark_class.__init__).parameters.keys())
    benchmark_init_params.discard("self")

    for key, value in optional_params.items():
        if key in benchmark_init_params:
            benchmark_kwargs[key] = value
        elif key == "tasks":
            # Backward compatibility: map general 'tasks' to known aliases.
            if "task" in benchmark_init_params:
                benchmark_kwargs["task"] = value
            elif "competitions" in benchmark_init_params:
                benchmark_kwargs["competitions"] = value

    benchmark: BaseBenchmark = benchmark_class(**benchmark_kwargs)

    # --- 4. Execute workflow ---
    runner.benchmark = benchmark
    eval_function = runner.get_eval_function()
    logger.info(f"Starting benchmark '{args.benchmark}' with workflow '{config.workflow.name}'...")
    await benchmark.run_evaluation(eval_fn=eval_function)

    # --- 5. Present results ---
    summary_table, totals_table = _build_benchmark_summary(
        getattr(benchmark, "results_path", None),
        runner.get_run_records()
    )

    if summary_table:
        renderables = [summary_table]
        if totals_table:
            renderables.append(totals_table)
        console.print(
            Panel(
                Group(*renderables),
                title="[bold green]Benchmark Run Summary[/bold green]",
                subtitle=f"Logs saved in: [cyan]{log_dir.resolve()}[/cyan]"
            )
        )
    else:
        console.print(
            Panel(
                f"All evaluation outputs and logs are saved in:\n[cyan]{log_dir.resolve()}[/cyan]",
                title="[bold green]Benchmark Run Finished[/bold green]"
            )
        )

    # --- 6. Cleanup pending tasks ---
    pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for t in pending:
        t.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
