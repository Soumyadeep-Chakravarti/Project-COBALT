# L02_FOUNDATION_LAYER/L02A_HostExecutionCore/sync_execution.py

import os
import subprocess
import time
from typing import List

# Import the contracts (Pydantic Models) from Layer 5
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_command import ExecutionCommand
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_result import ExecutionResult


def execute_sync(command_data: ExecutionCommand) -> ExecutionResult:
    """
    Executes a shell command synchronously (blocking).
    (The full implementation logic remains the same as previously drafted)
    """

    cmd_list: List[str] = [command_data.command] + command_data.args
    start_time = time.time()

    result_kwargs = {
        "status": "FAILURE",
        "exit_code": -1,
        "stdout": "",
        "stderr": "",
        "error_message": None,
    }

    try:
        completed_process = subprocess.run(
            cmd_list,
            cwd=command_data.cwd,
            timeout=command_data.timeout,
            env={**os.environ, **command_data.env_vars},
            check=False,
            capture_output=True,
            text=True,
        )

        result_kwargs["stdout"] = completed_process.stdout.strip()
        result_kwargs["stderr"] = completed_process.stderr.strip()
        result_kwargs["exit_code"] = completed_process.returncode

        if completed_process.returncode == 0:
            result_kwargs["status"] = "SUCCESS"
        else:
            result_kwargs["status"] = "FAILURE"
            result_kwargs["error_message"] = (
                f"Command exited with non-zero code {completed_process.returncode}."
            )

    except subprocess.TimeoutExpired as e:
        result_kwargs["status"] = "TIMEOUT"
        result_kwargs["error_message"] = (
            f"Command timed out after {command_data.timeout} seconds. Process was terminated."
        )
        result_kwargs["stdout"] = e.stdout.decode() if e.stdout else ""
        result_kwargs["stderr"] = e.stderr.decode() if e.stderr else ""

    except FileNotFoundError:
        result_kwargs["status"] = "FAILURE"
        result_kwargs["error_message"] = (
            f"Executable not found: {command_data.command}. Check PATH or cwd."
        )

    except Exception as e:
        result_kwargs["status"] = "FAILURE"
        result_kwargs["error_message"] = (
            f"Unexpected system error during execution: {type(e).__name__}: {str(e)}"
        )

    finally:
        duration = time.time() - start_time
        result_kwargs["duration_s"] = duration

        return ExecutionResult.model_validate(result_kwargs)
