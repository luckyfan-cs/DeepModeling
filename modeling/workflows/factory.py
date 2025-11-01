# modeling/workflows/factory.py

from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Optional

# --- Core configuration and interface imports ---
from modeling.config import ModelingConfig, LLMConfig
from modeling.workflows.base import ModelingWorkflow
from modeling.benchmark.benchmark import BaseBenchmark

# --- Services imports ---
from modeling.services.workspace import WorkspaceService
from modeling.services.llm import LLMService
from modeling.services.sandbox import SandboxService

# --- State management imports ---
from modeling.services.states.journal import JournalState

# --- Operators imports ---
from modeling.operators.llm_basic import GenerateCodeAndPlanOperator, ReviewOperator
from modeling.operators.code import ExecuteAndTestOperator

# --- Concrete workflow imports ---
from modeling.workflows.search.scientific_workflow import ScientificWorkflow

logger = logging.getLogger(__name__)


class WorkflowFactory(ABC):
    """
    Abstract base class for workflow factories.
    
    Defines a unified interface for creating workflow instances based on configuration.
    This follows the factory pattern, separating object creation logic from usage.
    """
    @abstractmethod
    def create_workflow(self, config: ModelingConfig, benchmark: Optional[BaseBenchmark] = None) -> ModelingWorkflow:
        """
        Create and return a configured workflow instance based on the provided configuration.

        Args:
            config: Complete ModelingConfig object containing all runtime parameters.

        Returns:
            A fully initialized ModelingWorkflow instance ready to execute solve() method.
        """
        raise NotImplementedError


# ==============================================================================
# ==                       SCIENTIFIC WORKFLOW FACTORY                         ==
# ==============================================================================
class ScientificWorkflowFactory(WorkflowFactory):
    """A specialized factory for creating and assembling ScientificWorkflow."""
    def create_workflow(self, config: ModelingConfig, benchmark: Optional[BaseBenchmark] = None) -> ScientificWorkflow:
        logger.info("ScientificWorkflowFactory: Assembling Scientific workflow...")

        workspace_base = None
        if config.workflow and config.workflow.params:
            workspace_base = config.workflow.params.get("workspace_base_dir")
        workspace = WorkspaceService(run_name=config.run.name, base_dir=workspace_base)
        llm_service = LLMService(config=config.llm)
        sandbox_service = SandboxService(workspace=workspace, timeout=config.sandbox.timeout)

        operators = {
            "generate": GenerateCodeAndPlanOperator(llm_service=llm_service),
            "execute": ExecuteAndTestOperator(sandbox_service=sandbox_service),
            "review": ReviewOperator(llm_service=llm_service),
        }

        services = {
            "llm": llm_service,
            "sandbox": sandbox_service,
            "workspace": workspace,
        }

        workflow = ScientificWorkflow(
            operators=operators,
            services=services,
            agent_config=config.agent.model_dump(),
            benchmark=benchmark
        )

        logger.info("Scientific workflow assembled successfully.")
        return workflow

