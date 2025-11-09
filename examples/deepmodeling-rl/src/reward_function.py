# examples/deepmodeling-rl/reward_function.py

"""Reward function for DeepModeling RL training.

The reward is calculated based on:
1. Execution success (did the experiment run without errors?)
2. Quality score from ReviewResult (how good is the solution?)
3. Thoroughness score from ReviewResult (how thorough is the analysis?)
4. Achievement bonus (did it pass the benchmark threshold?)
"""

from typing import Dict, Any, Optional, List
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modeling.models.formats import ReviewResult
from modeling.common.typing import ExecutionResult


class RewardCalculator:
    """Calculate rewards for DeepModeling RL training."""

    def __init__(
        self,
        base_execution_reward: float = 0.2,
        quality_weight: float = 0.5,
        thoroughness_weight: float = 0.3,
        achievement_bonus: float = 1.0,
        failure_penalty: float = -0.1,
    ):
        """Initialize reward calculator.

        Args:
            base_execution_reward: Reward for successful execution
            quality_weight: Weight for quality score (0-1)
            thoroughness_weight: Weight for thoroughness score (0-1)
            achievement_bonus: Bonus for passing benchmark threshold
            failure_penalty: Penalty for execution failure
        """
        self.base_execution_reward = base_execution_reward
        self.quality_weight = quality_weight
        self.thoroughness_weight = thoroughness_weight
        self.achievement_bonus = achievement_bonus
        self.failure_penalty = failure_penalty

    def calculate_reward(
        self,
        agent_output: Dict[str, Any],
        task_data: Dict[str, Any],
    ) -> float:
        """Calculate reward for an agent episode.

        Args:
            agent_output: Output from agent.run(), containing:
                - messages: List of conversation messages
                - success: Whether the task succeeded
                - last_review: ReviewResult object
                - task_id: Task identifier
            task_data: Original task data, containing:
                - threshold: Target threshold for success
                - eval_metric: Metric to evaluate

        Returns:
            Float reward value (typically 0.0 to 2.0)
        """
        reward = 0.0

        # Extract information
        success = agent_output.get("success", False)
        last_review = agent_output.get("last_review")

        # Check if we have experiments in the conversation
        has_experiment = self._check_for_experiments(agent_output.get("messages", []))

        # Base reward for execution
        if has_experiment:
            if success:
                reward += self.base_execution_reward
            else:
                reward += self.failure_penalty

        # Quality and thoroughness rewards
        if last_review:
            quality_score = last_review.quality_score if hasattr(last_review, 'quality_score') else 0.0
            thoroughness_score = last_review.thoroughness_score if hasattr(last_review, 'thoroughness_score') else 0.0

            reward += quality_score * self.quality_weight
            reward += thoroughness_score * self.thoroughness_weight

            # Achievement bonus
            if self._check_achievement(last_review, task_data):
                reward += self.achievement_bonus

        # Ensure non-negative reward
        reward = max(0.0, reward)

        return reward

    def _check_for_experiments(self, messages: List[Dict[str, str]]) -> bool:
        """Check if there are any experiments in the conversation."""
        for msg in messages:
            content = msg.get("content", "")
            if "<Experiment>" in content:
                return True
        return False

    def _check_achievement(
        self,
        review: ReviewResult,
        task_data: Dict[str, Any]
    ) -> bool:
        """Check if the solution achieves the target threshold.

        Args:
            review: ReviewResult from evaluation
            task_data: Task data with threshold

        Returns:
            True if achievement condition is met
        """
        # Check completion state
        if hasattr(review, 'completion_state'):
            if review.completion_state in ["complete", "excellent"]:
                return True

        # Check quality threshold
        if hasattr(review, 'quality_score'):
            threshold = task_data.get("threshold", 0.7)
            if review.quality_score >= threshold:
                return True

        # Check metric value if available
        if hasattr(review, 'metric_value') and review.metric_value is not None:
            threshold = task_data.get("threshold", 0.7)
            is_lower_better = getattr(review, 'lower_is_better', True)

            if is_lower_better:
                return review.metric_value <= threshold
            else:
                return review.metric_value >= threshold

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
            - execution: Execution reward
            - quality: Quality reward
            - thoroughness: Thoroughness reward
            - achievement: Achievement bonus
        """
        breakdown = {
            "total": 0.0,
            "execution": 0.0,
            "quality": 0.0,
            "thoroughness": 0.0,
            "achievement": 0.0,
        }

        success = agent_output.get("success", False)
        last_review = agent_output.get("last_review")
        has_experiment = self._check_for_experiments(agent_output.get("messages", []))

        # Execution reward
        if has_experiment:
            if success:
                breakdown["execution"] = self.base_execution_reward
            else:
                breakdown["execution"] = self.failure_penalty

        # Quality and thoroughness
        if last_review:
            quality_score = last_review.quality_score if hasattr(last_review, 'quality_score') else 0.0
            thoroughness_score = last_review.thoroughness_score if hasattr(last_review, 'thoroughness_score') else 0.0

            breakdown["quality"] = quality_score * self.quality_weight
            breakdown["thoroughness"] = thoroughness_score * self.thoroughness_weight

            # Achievement
            if self._check_achievement(last_review, task_data):
                breakdown["achievement"] = self.achievement_bonus

        # Calculate total
        breakdown["total"] = max(0.0, sum([
            breakdown["execution"],
            breakdown["quality"],
            breakdown["thoroughness"],
            breakdown["achievement"]
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
    print("Testing reward calculator...")

    # Mock ReviewResult
    class MockReview:
        def __init__(self):
            self.quality_score = 0.8
            self.thoroughness_score = 0.7
            self.completion_state = "complete"
            self.metric_value = 0.85
            self.lower_is_better = False

    # Test case 1: Successful execution with good scores
    agent_output_success = {
        "success": True,
        "last_review": MockReview(),
        "messages": [
            {"role": "assistant", "content": "<Experiment>\nprint('test')\n</Experiment>"}
        ],
        "task_id": "test-001"
    }

    task_data = {
        "threshold": 0.7,
        "eval_metric": "accuracy"
    }

    reward = calculate_reward(agent_output_success, task_data)
    breakdown = calculate_detailed_reward(agent_output_success, task_data)

    print(f"\nTest Case 1: Successful execution")
    print(f"Total Reward: {reward:.2f}")
    print(f"Breakdown: {json.dumps(breakdown, indent=2)}")

    # Test case 2: Failed execution
    agent_output_fail = {
        "success": False,
        "last_review": None,
        "messages": [
            {"role": "assistant", "content": "<Experiment>\ninvalid code\n</Experiment>"}
        ],
        "task_id": "test-002"
    }

    reward = calculate_reward(agent_output_fail, task_data)
    breakdown = calculate_detailed_reward(agent_output_fail, task_data)

    print(f"\nTest Case 2: Failed execution")
    print(f"Total Reward: {reward:.2f}")
    print(f"Breakdown: {json.dumps(breakdown, indent=2)}")

    # Test case 3: No experiments
    agent_output_no_exp = {
        "success": False,
        "last_review": None,
        "messages": [
            {"role": "assistant", "content": "I don't know how to solve this."}
        ],
        "task_id": "test-003"
    }

    reward = calculate_reward(agent_output_no_exp, task_data)
    breakdown = calculate_detailed_reward(agent_output_no_exp, task_data)

    print(f"\nTest Case 3: No experiments")
    print(f"Total Reward: {reward:.2f}")
    print(f"Breakdown: {json.dumps(breakdown, indent=2)}")

    print("\n✓ Reward calculator tests completed!")
