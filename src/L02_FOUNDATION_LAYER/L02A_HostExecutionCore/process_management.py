# L02_FOUNDATION_LAYER/L02A_HostExecutionCore/process_management.py

# 1. Import necessary contracts from Layer 5
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_command import ExecutionCommand
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_result import ExecutionResult

from .async_execution import execute_async

# 2. Import the specialized execution functions
from .sync_execution import execute_sync

# 3. Export the primary interface functions
# We use __all__ to define the public API of this module.
__all__ = [
    "ExecutionCommand",
    "ExecutionResult",
    "execute_sync",
    "execute_async",
]

# Note: No actual function logic is defined here. It is strictly a forwarding layer.
