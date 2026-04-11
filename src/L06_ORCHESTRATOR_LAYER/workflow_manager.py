# L06_ORCHESTRATOR_LAYER/workflow_manager.py

from typing import Any, Awaitable, Dict, List

from L02_FOUNDATION_LAYER.L02A_HostExecutionCore import (
    process_management as execution_core,
)
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_command import ExecutionCommand
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_result import ExecutionResult


class WorkflowManager:
    """
    Manages the sequencing, concurrency, and state tracking of COBALT execution jobs.
    This class is the consumer of the L02 HostExecutionCore functionality.
    """

    def __init__(self, job_config: Dict[str, Any]):
        """
        Initializes the manager with the overall configuration for the current job.
        """
        self.job_config = job_config
        self.current_state: Dict[str, Any] = {"status": "INITIALIZED", "results": {}}
        self.max_concurrent_tasks: int = job_config.get("max_concurrent_tasks", 10)
        self.task_semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

    # --- Core Execution Methods ---

    async def run_single_step(self, command_data: ExecutionCommand) -> ExecutionResult:
        """
        Executes a single command asynchronously, respecting the concurrency limit.
        """
        async with self.task_semaphore:
            # Note: We rely on the L02 core to handle the actual subprocess logic
            print(f"Executing step {command_data.context_id}...")
            result = await execution_core.execute_async(command_data)
            self.current_state["results"][command_data.context_id] = result.model_dump()
            return result

    async def run_workflow(
        self, command_list: List[ExecutionCommand]
    ) -> Dict[str, Any]:
        """
        Executes a list of commands, potentially in parallel where possible,
        and manages the overall workflow based on success/failure.

        This is where true orchestration logic (e.g., error handling, conditional execution)
        would be implemented, but for now, we demonstrate simple concurrent execution.
        """
        self.current_state["status"] = "RUNNING"

        # 1. Create a list of tasks (coroutines)
        tasks: List[Awaitable[ExecutionResult]] = [
            self.run_single_step(cmd) for cmd in command_list
        ]

        # 2. Run tasks concurrently and wait for all to complete
        try:
            # asyncio.gather executes all tasks concurrently
            results: List[ExecutionResult] = await asyncio.gather(*tasks)

            # Check results for overall status
            if any(r.status != "SUCCESS" for r in results):
                self.current_state["status"] = "COMPLETED_WITH_ERRORS"
            else:
                self.current_state["status"] = "SUCCESS"

        except Exception as e:
            self.current_state["status"] = "FATAL_ERROR"
            self.current_state["error"] = (
                f"An unexpected error occurred during workflow execution: {e}"
            )

        return self.current_state


# We'll need to import asyncio within the module for the Semaphore and gather to work
import asyncio
