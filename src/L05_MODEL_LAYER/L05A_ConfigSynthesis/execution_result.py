# L05_MODEL_LAYER/L05A_ConfigSynthesis/execution_result.py
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    """
    Defines the standard output contract for the result of a host execution.
    """

    status: Literal["SUCCESS", "FAILURE", "TIMEOUT", "ERROR"] = Field(
        ..., description="The terminal state of the command execution."
    )
    exit_code: int = Field(
        ...,
        description="The integer return code from the operating system. -1 if not available.",
    )
    duration_s: float = Field(
        ..., ge=0, description="The total time elapsed during execution in seconds."
    )
    stdout: str = Field(
        ..., description="The captured standard output from the command."
    )
    stderr: str = Field(
        ..., description="The captured standard error output from the command."
    )
    error_message: Optional[str] = Field(
        None,
        description="A detailed message only present if status is FAILURE, TIMEOUT, or ERROR.",
    )

    class Config:
        title = "ExecutionResultSchema"
