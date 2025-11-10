#!/usr/bin/env python3
"""
Main entry point for DeepModeling inference - Compatible with existing workflow.

Usage:
    python main.py --workflow scientific --benchmark mathmodeling \
        --data-dir "/path/to/data" \
        --llm-model openai/deepseek-ai/DeepSeek-V3-Terminus \
        --task mathmodeling-0

    python main.py --workflow scientific --benchmark engineering \
        --llm-api http://localhost:8000 \
        --task industry-0
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import DeepModelingInferenceAgent, load_benchmark_tasks


def parse_args():
    parser = argparse.ArgumentParser(
        description="DeepModeling Inference - Test trained SFT/RL models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using API endpoint
  python main.py --workflow scientific --benchmark engineering \\
      --llm-api http://localhost:8000 --task industry-0

  # Using OpenAI-style model name
  python main.py --workflow scientific --benchmark mathmodeling \\
      --llm-model openai/deepseek-ai/DeepSeek-V3-Terminus \\
      --task mathmodeling-0

  # Batch testing
  python main.py --workflow scientific --benchmark engineering \\
      --llm-api http://localhost:8000 --task-limit 5
        """
    )

    # Workflow configuration
    parser.add_argument(
        "--workflow",
        default="scientific",
        choices=["scientific"],
        help="Workflow type (default: scientific)"
    )
    
    parser.add_argument(
        "--benchmark",
        required=True,
        choices=["engineering", "mathmodeling", "science", "mle"],
        help="Benchmark to use for testing"
    )
    
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Data directory for benchmark (optional, will use default if not specified)"
    )

    # LLM configuration (choose one)
    llm_group = parser.add_mutually_exclusive_group(required=True)
    llm_group.add_argument(
        "--llm-model",
        type=str,
        help="LLM model name (e.g., openai/deepseek-ai/DeepSeek-V3-Terminus)"
    )
    llm_group.add_argument(
        "--llm-api",
        type=str,
        help="LLM API endpoint (e.g., http://localhost:8000)"
    )

    # Task selection (choose one)
    task_group = parser.add_mutually_exclusive_group(required=True)
    task_group.add_argument(
        "--task",
        type=str,
        help="Single task ID to run (e.g., industry-0, mathmodeling-0)"
    )
    task_group.add_argument(
        "--competitions",
        nargs="+",
        help="List of competition IDs to run"
    )
    task_group.add_argument(
        "--task-limit",
        type=int,
        help="Number of tasks to run (random selection)"
    )

    # Agent configuration
    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
        help="Maximum number of turns per task (default: 10)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0 for greedy)"
    )
    
    parser.add_argument(
        "--sandbox-timeout",
        type=int,
        default=600,
        help="Sandbox execution timeout in seconds (default: 600)"
    )

    # Output configuration
    parser.add_argument(
        "--workspace-dir",
        type=Path,
        default=Path("./workspace_infer"),
        help="Workspace directory (default: ./workspace_infer)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./results"),
        help="Output directory for results (default: ./results)"
    )

    # Advanced options
    parser.add_argument(
        "--use-local-model",
        action="store_true",
        help="Load model locally instead of using API"
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Configure logging
    import logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='[%(levelname)s] %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Print configuration
    print("=" * 80)
    print("DeepModeling Inference")
    print("=" * 80)
    print(f"Workflow: {args.workflow}")
    print(f"Benchmark: {args.benchmark}")
    
    if args.llm_api:
        print(f"LLM API: {args.llm_api}")
        api_endpoint = args.llm_api

        # Query vLLM to get the actual model name
        try:
            import requests
            response = requests.get(f"{args.llm_api}/v1/models", timeout=5)
            response.raise_for_status()
            models_data = response.json()

            # vLLM returns a list of models
            if models_data.get("data") and len(models_data["data"]) > 0:
                model_path = models_data["data"][0]["id"]
                logger.info(f"Auto-detected model from API: {model_path}")
            else:
                # Fallback: use a generic name, will be ignored by API
                model_path = "default"
                logger.warning("Could not detect model name from API, using 'default'")
        except Exception as e:
            logger.warning(f"Could not query API for model name: {e}")
            model_path = "default"
    else:
        print(f"LLM Model: {args.llm_model}")
        model_path = args.llm_model
        # Try to infer API endpoint from model name
        # Assume format: openai/provider/model-name means use OpenAI API
        if args.llm_model.startswith("openai/"):
            api_endpoint = "https://api.openai.com"  # Or configured endpoint
            logger.info("Detected OpenAI model format, will use OpenAI API")
        else:
            api_endpoint = None
    
    print(f"Max turns: {args.max_turns}")
    print(f"Temperature: {args.temperature}")
    print("=" * 80)
    print()

    # Load tasks
    logger.info(f"Loading tasks from benchmark: {args.benchmark}")
    
    if args.task:
        # Single task
        tasks = load_benchmark_tasks(
            benchmark=args.benchmark,
            data_root=args.data_dir,
            competitions=[args.task],
            limit=1,
        )
        logger.info(f"Loaded single task: {args.task}")
    elif args.competitions:
        # Multiple specific tasks
        tasks = load_benchmark_tasks(
            benchmark=args.benchmark,
            data_root=args.data_dir,
            competitions=args.competitions,
        )
        logger.info(f"Loaded {len(tasks)} tasks from specified competitions")
    else:
        # Random tasks with limit
        tasks = load_benchmark_tasks(
            benchmark=args.benchmark,
            data_root=args.data_dir,
            limit=args.task_limit,
        )
        logger.info(f"Loaded {len(tasks)} tasks (limit: {args.task_limit})")

    if not tasks:
        logger.error("No tasks loaded! Check your benchmark and data directory.")
        return 1

    # Create agent
    logger.info("Creating inference agent...")
    agent = DeepModelingInferenceAgent(
        model_path=model_path,
        api_endpoint=api_endpoint,
        max_turns=args.max_turns,
        workspace_dir=str(args.workspace_dir),
        sandbox_timeout=args.sandbox_timeout,
        temperature=args.temperature,
        use_local_model=args.use_local_model,
    )

    # Run inference
    results = []
    for i, task in enumerate(tasks):
        print()
        print("=" * 80)
        print(f"Task {i+1}/{len(tasks)}: {task['task_id']}")
        print("=" * 80)
        
        try:
            result = agent.run_inference(task)
            results.append(result)
            
            print()
            print(f"✓ Task completed:")
            print(f"  Success: {result['success']}")
            print(f"  Turns: {result['num_turns']}")
            print(f"  Grade: {result.get('grade_score', 'N/A')}")
            print(f"  Duration: {result['duration_seconds']:.2f}s")
            
        except Exception as e:
            logger.error(f"Failed to run task {task['task_id']}: {e}", exc_info=True)
            results.append({
                "task_id": task["task_id"],
                "success": False,
                "error": str(e),
            })
            print(f"✗ Task failed: {e}")

    # Save summary
    import json
    from datetime import datetime
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / f"summary_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

    summary = {
        "workflow": args.workflow,
        "benchmark": args.benchmark,
        "llm": args.llm_model or args.llm_api,
        "total_tasks": len(tasks),
        "successful": sum(1 for r in results if r.get("success", False)),
        "failed": sum(1 for r in results if not r.get("success", False)),
        "avg_turns": sum(r.get("num_turns", 0) for r in results) / len(results) if results else 0,
        "avg_grade": sum(r.get("grade_score", 0) for r in results if r.get("grade_score") is not None) /
                     max(1, sum(1 for r in results if r.get("grade_score") is not None)),
        "results": results,
        "config": {
            "max_turns": args.max_turns,
            "temperature": args.temperature,
            "sandbox_timeout": args.sandbox_timeout,
        }
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print final summary
    print()
    print("=" * 80)
    print("INFERENCE COMPLETE")
    print("=" * 80)
    print(f"Total tasks: {summary['total_tasks']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success rate: {summary['successful'] / summary['total_tasks'] * 100:.1f}%")
    print(f"Average turns: {summary['avg_turns']:.2f}")
    
    if summary['avg_grade'] > 0:
        print(f"Average grade: {summary['avg_grade']:.4f}")
    
    print()
    print(f"Summary saved to: {summary_path}")
    print(f"Workspaces saved to: {args.workspace_dir}/")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
