# L05_MODEL_LAYER/L05A_ConfigSynthesis/execution_command.py
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExecutionCommand(BaseModel):
    """
    Defines the complete input contract for a host execution request.
    """

    command: str = Field(..., description="The executable name or script to run.")
    args: List[str] = Field(
        default_factory=list, description="A list of arguments for the command."
    )
    cwd: Optional[str] = Field(
        None, description="The current working directory to execute the command from."
    )
    timeout: float = Field(
        default=300.0,
        gt=0,
        description="Maximum execution time in seconds (must be positive).",
    )
    env_vars: Dict[str, str] = Field(
        default_factory=dict,
        description="A dictionary of environment variables to set/override.",
    )
    # New Field for Context/Logging
    context_id: str = Field(
        ..., description="A unique identifier for tracking this specific execution job."
    )

    class Config:
        # Ensures models can be used with internal tools and documentation
        title = "ExecutionCommandSchema"

