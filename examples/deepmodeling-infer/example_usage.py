#!/usr/bin/env python3
"""Example usage of DeepModeling Inference Framework."""

from pathlib import Path
from src import (
    DeepModelingInferenceAgent,
    load_benchmark_tasks,
    create_infer_config,
)

def example_api_inference():
    """Example: Using API endpoint for inference."""
    
    print("=" * 80)
    print("Example 1: API-based Inference")
    print("=" * 80)
    
    # Create agent with API endpoint
    agent = DeepModelingInferenceAgent(
        model_path="Qwen/Qwen2.5-7B-Instruct",  # Model name
        api_endpoint="http://localhost:8000",    # vLLM endpoint
        max_turns=5,
        temperature=0.0,
        workspace_dir="./workspace_example",
    )
    
    # Load a single task
    tasks = load_benchmark_tasks(
        benchmark="engineering",
        competitions=["industry-0"],
        limit=1,
    )
    
    if tasks:
        print(f"\nRunning inference on task: {tasks[0]['task_id']}")
        result = agent.run_inference(tasks[0])
        
        print(f"\nResults:")
        print(f"  Success: {result['success']}")
        print(f"  Turns: {result['num_turns']}")
        print(f"  Grade: {result.get('grade_score', 'N/A')}")
        print(f"  Duration: {result['duration_seconds']:.2f}s")


def example_local_inference():
    """Example: Using local model for inference."""
    
    print("\n" + "=" * 80)
    print("Example 2: Local Model Inference")
    print("=" * 80)
    
    # Create agent with local model
    agent = DeepModelingInferenceAgent(
        model_path="/path/to/your/model",
        use_local_model=True,
        max_turns=5,
        temperature=0.0,
        workspace_dir="./workspace_example",
    )
    
    # Load tasks
    tasks = load_benchmark_tasks(
        benchmark="engineering",
        limit=2,
    )
    
    results = []
    for task in tasks:
        print(f"\nProcessing: {task['task_id']}")
        result = agent.run_inference(task)
        results.append(result)
        
        print(f"  Success: {result['success']}")
        print(f"  Grade: {result.get('grade_score', 'N/A')}")
    
    # Calculate statistics
    successful = sum(1 for r in results if r['success'])
    avg_grade = sum(r.get('grade_score', 0) for r in results if r.get('grade_score')) / max(1, len([r for r in results if r.get('grade_score')]))
    
    print(f"\nOverall:")
    print(f"  Total: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Avg Grade: {avg_grade:.4f}")


def example_batch_inference():
    """Example: Batch inference on multiple tasks."""
    
    print("\n" + "=" * 80)
    print("Example 3: Batch Inference")
    print("=" * 80)
    
    # Configuration
    config = create_infer_config(
        api_endpoint="http://localhost:8000",
        max_turns=8,
        temperature=0.0,
        benchmark="engineering",
    )
    
    # Create agent
    agent = DeepModelingInferenceAgent(
        api_endpoint=config["model"]["api_endpoint"],
        max_turns=config["agent"]["max_turns"],
        temperature=config["agent"]["temperature"],
        workspace_dir=config["workspace"]["base_dir"],
    )
    
    # Load multiple tasks
    tasks = load_benchmark_tasks(
        benchmark=config["benchmark"]["name"],
        competitions=["industry-0", "industry-1", "industry-2"],
    )
    
    print(f"\nLoaded {len(tasks)} tasks")
    print("Running batch inference...")
    
    results = []
    for i, task in enumerate(tasks):
        print(f"\n[{i+1}/{len(tasks)}] {task['task_id']}")
        try:
            result = agent.run_inference(task)
            results.append(result)
            print(f"  ✓ Success: {result['success']}, Grade: {result.get('grade_score', 'N/A')}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            results.append({"task_id": task["task_id"], "success": False, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 80)
    print("Batch Inference Summary")
    print("=" * 80)
    print(f"Total tasks: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r.get('success'))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
    
    grades = [r.get('grade_score') for r in results if r.get('grade_score') is not None]
    if grades:
        print(f"Average grade: {sum(grades) / len(grades):.4f}")
        print(f"Min grade: {min(grades):.4f}")
        print(f"Max grade: {max(grades):.4f}")


def example_custom_config():
    """Example: Using custom configuration."""
    
    print("\n" + "=" * 80)
    print("Example 4: Custom Configuration")
    print("=" * 80)
    
    # Custom configuration
    custom_config = {
        "model": {
            "path": "your-custom-model",
            "api_endpoint": "http://custom-endpoint:8000",
        },
        "agent": {
            "max_turns": 15,
            "temperature": 0.3,
            "sandbox_timeout": 900,
        },
        "workspace": {
            "base_dir": "./custom_workspace",
        },
        "benchmark": {
            "name": "science",
            "data_root": "/custom/path/to/data",
        },
    }
    
    print("\nCustom configuration:")
    print(f"  Model: {custom_config['model']['path']}")
    print(f"  Max turns: {custom_config['agent']['max_turns']}")
    print(f"  Temperature: {custom_config['agent']['temperature']}")
    print(f"  Benchmark: {custom_config['benchmark']['name']}")
    
    # Create agent with custom config
    agent = DeepModelingInferenceAgent(
        model_path=custom_config["model"]["path"],
        api_endpoint=custom_config["model"]["api_endpoint"],
        max_turns=custom_config["agent"]["max_turns"],
        temperature=custom_config["agent"]["temperature"],
        sandbox_timeout=custom_config["agent"]["sandbox_timeout"],
        workspace_dir=custom_config["workspace"]["base_dir"],
    )
    
    print("\nAgent created successfully!")
    print("Ready for inference with custom settings.")


if __name__ == "__main__":
    print("DeepModeling Inference - Usage Examples")
    print("=" * 80)
    print()
    print("This script demonstrates various ways to use the inference framework.")
    print("Uncomment the example you want to run.")
    print()
    
    # Uncomment the example you want to run:
    
    # Example 1: API-based inference (recommended)
    # example_api_inference()
    
    # Example 2: Local model inference
    # example_local_inference()
    
    # Example 3: Batch inference
    # example_batch_inference()
    
    # Example 4: Custom configuration
    # example_custom_config()
    
    print("\nTo run an example, uncomment it in this script and run:")
    print("  python example_usage.py")
    print()
    print("Or use the command-line interface:")
    print("  python -m src.infer --help")
