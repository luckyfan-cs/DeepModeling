from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# --- Pydantic Models for Operator Outputs ---
# These models are used with LLMService.call_with_json

class ReviewResult(BaseModel):
    """Structured result from the ReviewOperator."""
    is_buggy: bool = Field(..., description="True if the execution failed or has a clear bug, otherwise False.")
    summary: str = Field(..., description="If buggy, a proposal to fix the bug. If successful, a summary of empirical findings.")
    metric_value: Optional[float] = Field(..., description="A quantitative measure of success based on the task requirements. Null if the task does not define a quantitative metric or if it cannot be determined.")
    lower_is_better: bool = Field(default=True, description="True if a lower metric is better (e.g., RMSE), False if higher is better (e.g., Accuracy).")
    completion_state: Literal["blocked", "in_progress", "partial", "complete", "excellent", "unknown"] = Field(
        default="unknown",
        description="Reviewer judgment of current completion status."
    )
    quality_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Normalized (0.0-1.0) score reflecting solution quality/performance."
    )
    thoroughness_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Normalized (0.0-1.0) score reflecting depth of analysis or coverage."
    )
    should_continue: bool = Field(
        default=True,
        description="True if reviewer recommends another iteration for improvements or corrections."
    )
    improvement_notes: Optional[str] = Field(
        default=None,
        description="Key follow-up actions if the reviewer recommends continuing."
    )

class Task(BaseModel):
    """A single task within a larger plan."""
    task_id: str = Field(..., description="Unique identifier for a task, e.g., '1', '2.1'.")
    instruction: str = Field(..., description="Clear, concise instruction for what to do in this task.")
    dependent_task_ids: List[str] = Field(default_factory=list, description="List of task_ids this task depends on.")

class Plan(BaseModel):
    """A structured plan consisting of multiple tasks."""
    tasks: List[Task] = Field(..., description="A list of tasks to achieve the overall goal.")
