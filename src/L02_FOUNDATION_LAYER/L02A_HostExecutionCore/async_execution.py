import asyncio
import os
import time
from typing import Dict, List, Union

# Import the contracts (Pydantic Models) from Layer 5
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_command import ExecutionCommand
from L05_MODEL_LAYER.L05A_ConfigSynthesis.execution_result import ExecutionResult


# --- Helper Function to Clean Up Processes on Timeout ---
def _terminate_process(process: asyncio.subprocess.Process):
    """Attempt to terminate the process gently, then forcefully."""
    if process.returncode is None:
        try:
            # 1. Try sending SIGTERM (Standard termination request)
            process.terminate()
            # 2. Wait a small period for graceful exit
            # Note: In a real asyncio loop, we'd use 'await asyncio.sleep(0.1)'
            # but since this is a utility function called within an exception block,
            # we rely on the loop's natural flow or a forceful action below.

            # 3. If still running, kill it
            # In a clean asyncio implementation, the process would be awaited
            # after terminate, but for robustness against a dead process:
            # We'll just rely on the main coroutine's cancellation handling
            # to clean up, but we'll add a quick kill for absolute certainty.
            if process.returncode is None:
                process.kill()
        except Exception:
            # Ignore errors if the process is already gone
            pass


# --- Primary Asynchronous Execution Function ---
async def execute_async(command_data: ExecutionCommand) -> ExecutionResult:
    """
    Executes a shell command asynchronously (non-blocking) using asyncio.

    The timeout is handled by asyncio.wait_for, which raises a TimeoutError
    and allows for proper cleanup (termination/killing) of the spawned process.
    """
    cmd_list: List[str] = [command_data.command] + command_data.args
    start_time = time.time()

    # Environment variable preparation
    env_vars: Dict[str, str] = {**os.environ, **command_data.env_vars}

    result_kwargs: Dict[str, Union[str, int, float, None]] = {
        "status": "FAILURE",
        "exit_code": -1,
        "stdout": "",
        "stderr": "",
        "error_message": None,
        "duration_s": 0.0,
    }

    process = None
    stdout_bytes, stderr_bytes = b"", b""

    try:
        # 1. Create the Subprocess (Non-blocking I/O with PIPE)
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            cwd=command_data.cwd,
            env=env_vars,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # 2. Wait for process completion or timeout
        try:
            # asyncio.communicate() handles the reading of stdout/stderr pipes
            # and waits for the process to exit, preventing deadlocks.
            # asyncio.wait_for() handles the overall timeout.
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(), timeout=command_data.timeout
            )

            # Process exited within the timeout
            result_kwargs["exit_code"] = process.returncode

        except asyncio.TimeoutError:
            # The communicate call timed out
            result_kwargs["status"] = "TIMEOUT"
            result_kwargs["error_message"] = (
                f"Command timed out after {command_data.timeout} seconds."
            )

            # Process cleanup: Must attempt to terminate/kill the lingering process
            if process:
                _terminate_process(process)

            # Re-read whatever was written to the pipes before the timeout
            # Note: process.communicate() consumes the output, so this may be empty,
            # but it is best practice to re-check if we were able to read before cancellation.
            # We will use what was captured before the TimeoutError if available.
            # The official asyncio documentation suggests capturing partial results
            # is complex. For COBALT, we'll accept the result of communicate()
            # being partially or fully lost on timeout for simplicity,
            # prioritizing the process exit guarantee.
            pass  # We rely on stdout_bytes/stderr_bytes being what was captured before TimeoutError

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
            if process:
                _terminate_process(
                    process
                )  # Ensure process is killed on any unexpected exception

    except Exception as e:
        # Handle exceptions during subprocess creation (e.g., Command not found)
        result_kwargs["status"] = "FAILURE"
        result_kwargs["error_message"] = (
            f"Failed to start process: {type(e).__name__}: {str(e)}"
        )

    finally:
        # Finalize the result object
        duration = time.time() - start_time
        result_kwargs["duration_s"] = duration

        # Decode and clean up output
        if stdout_bytes:
            result_kwargs["stdout"] = stdout_bytes.decode(errors="ignore").strip()
        if stderr_bytes:
            result_kwargs["stderr"] = stderr_bytes.decode(errors="ignore").strip()

        # Final status check (only if not already TIMEOUT/FAILURE)
        if (
            result_kwargs["status"] not in ["TIMEOUT", "FAILURE"]
            and process
            and process.returncode is not None
        ):
            if process.returncode == 0:
                result_kwargs["status"] = "SUCCESS"
            else:
                result_kwargs["status"] = "FAILURE"
                if not result_kwargs["error_message"]:
                    result_kwargs["error_message"] = (
                        f"Command exited with non-zero code {process.returncode}."
                    )

        return ExecutionResult.model_validate(result_kwargs)
