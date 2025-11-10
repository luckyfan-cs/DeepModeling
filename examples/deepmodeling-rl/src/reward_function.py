# examples/deepmodeling-rl/reward_function.py

"""Simplified Reward function for DeepModeling RL training.

The reward is calculated based on 3 simple components:
1. Code execution success (did the experiment run without errors?)
2. Got a score (did the submission get graded successfully?)
3. Score quality (how good is the score? normalized to higher-is-better)

Note: grade_score from BenchmarkGrader is already normalized to "higher is better" format.
"""

from typing import Dict, Any, Optional, List
import json
from pathlib import Path


class RewardCalculator:
    """Calculate rewards for DeepModeling RL training based on execution and benchmark score."""

    def __init__(
        self,
        execution_reward: float = 0.3,
        got_score_reward: float = 0.2,
        score_weight: float = 1.0,
        execution_failure_penalty: float = -0.1,
    ):
        """Initialize reward calculator.

        Args:
            execution_reward: Reward for successful code execution (default 0.3)
            got_score_reward: Reward for getting a valid grade score (default 0.2)
            score_weight: Weight for the normalized grade score (default 1.0)
            execution_failure_penalty: Penalty for execution failure (default -0.1)
        """
        self.execution_reward = execution_reward
        self.got_score_reward = got_score_reward
        self.score_weight = score_weight
        self.execution_failure_penalty = execution_failure_penalty

    def calculate_reward(
        self,
        agent_output: Dict[str, Any],
        task_data: Dict[str, Any],
    ) -> float:
        """Calculate reward for an agent episode.

        Args:
            agent_output: Output from agent.run(), containing:
                - messages: List of conversation messages
                - success: Whether code execution succeeded
                - grade_score: Normalized benchmark score (higher is better, or None)
            task_data: Original task data (not used in simplified version)

        Returns:
            Float reward value (typically -0.1 to 1.5+)
        """
        reward = 0.0

        # 1. Code execution success
        success = agent_output.get("success", False)
        has_experiment = self._check_for_experiments(agent_output.get("messages", []))

        if has_experiment:
            if success:
                reward += self.execution_reward
            else:
                reward += self.execution_failure_penalty

        # 2. Got a valid grade score
        grade_score = agent_output.get("grade_score")
        if grade_score is not None:
            reward += self.got_score_reward

            # 3. Score quality (already normalized to higher-is-better by BenchmarkGrader)
            reward += grade_score * self.score_weight

        # Ensure non-negative total reward
        reward = max(0.0, reward)

        return reward

    def _check_for_experiments(self, messages: List[Dict[str, str]]) -> bool:
        """Check if there are any experiments in the conversation."""
        for msg in messages:
            content = msg.get("content", "")
            if "<Experiment>" in content:
                return True
        return False

    def calculate_detailed_reward(
        self,
        agent_output: Dict[str, Any],
        task_data: Dict[str, Any],
    ) -> Dict[str, float]:
        """Calculate detailed reward breakdown for logging.

        Returns:
            Dictionary with reward components:
            - total: Total reward
            - execution: Execution success/failure reward
            - got_score: Reward for obtaining a valid score
            - score_quality: Weighted grade score
        """
        breakdown = {
            "total": 0.0,
            "execution": 0.0,
            "got_score": 0.0,
            "score_quality": 0.0,
        }

        success = agent_output.get("success", False)
        has_experiment = self._check_for_experiments(agent_output.get("messages", []))
        grade_score = agent_output.get("grade_score")

        # 1. Execution reward/penalty
        if has_experiment:
            if success:
                breakdown["execution"] = self.execution_reward
            else:
                breakdown["execution"] = self.execution_failure_penalty

        # 2. Got score reward
        if grade_score is not None:
            breakdown["got_score"] = self.got_score_reward

            # 3. Score quality
            breakdown["score_quality"] = grade_score * self.score_weight

        # Calculate total
        breakdown["total"] = max(0.0, sum([
            breakdown["execution"],
            breakdown["got_score"],
            breakdown["score_quality"]
        ]))

        return breakdown


# Singleton instance for consistent reward calculation
default_reward_calculator = RewardCalculator()


def calculate_reward(
    agent_output: Dict[str, Any],
    task_data: Dict[str, Any],
) -> float:
    """Convenience function to calculate reward using default calculator.

    Args:
        agent_output: Output from agent.run()
        task_data: Original task data

    Returns:
        Float reward value
    """
    return default_reward_calculator.calculate_reward(agent_output, task_data)


def calculate_detailed_reward(
    agent_output: Dict[str, Any],
    task_data: Dict[str, Any],
) -> Dict[str, float]:
    """Convenience function to calculate detailed reward breakdown.

    Args:
        agent_output: Output from agent.run()
        task_data: Original task data

    Returns:
        Dictionary with reward components
    """
    return default_reward_calculator.calculate_detailed_reward(agent_output, task_data)


# Example usage and testing
if __name__ == "__main__":
    # Test reward calculation
    print("Testing simplified reward calculator...")
    print("=" * 60)

    task_data = {}  # Not used in simplified version

    # Test case 1: Successful execution with high grade score
    print("\nTest Case 1: Successful execution + high grade score (0.95)")
    agent_output_1 = {
        "success": True,
        "grade_score": 0.95,  # High normalized score
        "messages": [
            {"role": "assistant", "content": "<Experiment>\nprint('test')\n</Experiment>"}
        ],
        "task_id": "test-001"
    }
    reward_1 = calculate_reward(agent_output_1, task_data)
    breakdown_1 = calculate_detailed_reward(agent_output_1, task_data)
    print(f"Total Reward: {reward_1:.3f}")
    print(f"Breakdown: {json.dumps(breakdown_1, indent=2)}")

    # Test case 2: Successful execution with low grade score
    print("\nTest Case 2: Successful execution + low grade score (0.15)")
    agent_output_2 = {
        "success": True,
        "grade_score": 0.15,  # Low normalized score
        "messages": [
            {"role": "assistant", "content": "<Experiment>\nprint('test')\n</Experiment>"}
        ],
        "task_id": "test-002"
    }
    reward_2 = calculate_reward(agent_output_2, task_data)
    breakdown_2 = calculate_detailed_reward(agent_output_2, task_data)
    print(f"Total Reward: {reward_2:.3f}")
    print(f"Breakdown: {json.dumps(breakdown_2, indent=2)}")

    # Test case 3: Successful execution but no grade score
    print("\nTest Case 3: Successful execution but no grade (None)")
    agent_output_3 = {
        "success": True,
        "grade_score": None,  # Failed to grade
        "messages": [
            {"role": "assistant", "content": "<Experiment>\nprint('test')\n</Experiment>"}
        ],
        "task_id": "test-003"
    }
    reward_3 = calculate_reward(agent_output_3, task_data)
    breakdown_3 = calculate_detailed_reward(agent_output_3, task_data)
    print(f"Total Reward: {reward_3:.3f}")
    print(f"Breakdown: {json.dumps(breakdown_3, indent=2)}")

    # Test case 4: Failed execution
    print("\nTest Case 4: Failed execution")
    agent_output_4 = {
        "success": False,
        "grade_score": None,
        "messages": [
            {"role": "assistant", "content": "<Experiment>\ninvalid code\n</Experiment>"}
        ],
        "task_id": "test-004"
    }
    reward_4 = calculate_reward(agent_output_4, task_data)
    breakdown_4 = calculate_detailed_reward(agent_output_4, task_data)
    print(f"Total Reward: {reward_4:.3f}")
    print(f"Breakdown: {json.dumps(breakdown_4, indent=2)}")

    # Test case 5: No experiments
    print("\nTest Case 5: No experiments at all")
    agent_output_5 = {
        "success": False,
        "grade_score": None,
        "messages": [
            {"role": "assistant", "content": "I don't know how to solve this."}
        ],
        "task_id": "test-005"
    }
    reward_5 = calculate_reward(agent_output_5, task_data)
    breakdown_5 = calculate_detailed_reward(agent_output_5, task_data)
    print(f"Total Reward: {reward_5:.3f}")
    print(f"Breakdown: {json.dumps(breakdown_5, indent=2)}")

    print("\n" + "=" * 60)
    print("✓ Reward calculator tests completed!")
    print("\nReward formula: max(0, execution + got_score + score_quality)")
    print("  - execution: +0.3 (success) or -0.1 (failure)")
    print("  - got_score: +0.2 (if grade_score is not None)")
    print("  - score_quality: grade_score × 1.0")
