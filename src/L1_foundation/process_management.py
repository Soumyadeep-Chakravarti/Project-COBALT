import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple, Union

import psutil  # A common system management library for diagnostics

from utils.structured_logger import LoggerManager

# Initialize the logger for this specific module
logger = LoggerManager.get_logger("PROCESS_MANAGEMENT")

# --- Process Execution Result Type ---
ExecutionResult = Dict[str, Union[int, str, bool, float]]


class ProcessManagement:
    """
    Provides robust control over system processes, command execution, and diagnostics.
    Focuses on Layer 1 control: Runtime and Execution.
    """

    @staticmethod
    def run_command_sync(
        command: Union[str, List[str]],
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> ExecutionResult:
        """
        Executes a command synchronously (blocking) and waits for it to complete.

        Args:
            command: The command to execute (as a string or list of arguments).
            cwd: Optional working directory for the command.
            timeout: Maximum time in seconds to wait for the command.
            env_vars: Environment variables to set for the process.

        Returns:
            A dictionary containing the return code, stdout, and stderr.
        """
        is_shell = isinstance(command, str)

        try:
            # Prepare environment variables: inherit current environment + user defined
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            # subprocess.run is safer than Popen for simple synchronous execution
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # We handle the return code explicitly
                cwd=cwd,
                timeout=timeout,
                shell=is_shell,
                env=env,
            )

            success = result.returncode == 0

            log_data = {
                "action": "RUN_SYNC",
                "command": command,
                "cwd": cwd,
                "return_code": result.returncode,
                "success": success,
                "stdout_preview": result.stdout[:200].strip(),
                "stderr_preview": result.stderr[:200].strip(),
            }

            if success:
                logger.info("Command executed successfully.", extra_data=log_data)
            else:
                logger.error("Command failed.", extra_data=log_data)

            return {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": success,
            }

        except FileNotFoundError:
            logger.error(
                f"Command not found: {command}", extra_data={"action": "RUN_SYNC_FAIL"}
            )
            return {
                "return_code": 127,
                "stdout": "",
                "stderr": "Command not found.",
                "success": False,
            }
        except subprocess.TimeoutExpired:
            logger.error(
                f"Command timed out after {timeout}s: {command}",
                extra_data={"action": "RUN_SYNC_FAIL"},
            )
            return {
                "return_code": 124,
                "stdout": "",
                "stderr": "Execution timeout expired.",
                "success": False,
            }
        except Exception:
            logger.exception(
                f"Unexpected error executing command: {command}",
                extra_data={"action": "RUN_SYNC_FAIL"},
            )
            return {
                "return_code": 1,
                "stdout": "",
                "stderr": "Unexpected execution error.",
                "success": False,
            }

    @staticmethod
    def run_command_async(
        command: Union[str, List[str]],
        cwd: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ) -> Optional[subprocess.Popen]:
        """
        Executes a command asynchronously (non-blocking) and returns the Popen object.
        COBALT must manage this process lifecycle separately.

        Args:
            command: The command to execute.
            cwd: Optional working directory.
            env_vars: Environment variables to set for the process.

        Returns:
            The Popen object on success, or None on failure.
        """
        is_shell = isinstance(command, str)

        try:
            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)

            process = subprocess.Popen(
                command,
                cwd=cwd,
                shell=is_shell,
                env=env,
                # Direct stdout/stderr capture is often tricky for long-running async processes.
                # For simplicity here, we let it inherit the parent's standard streams,
                # but a robust system would pipe them to a file or socket.
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            logger.info(
                f"Asynchronous process launched successfully.",
                extra_data={
                    "action": "RUN_ASYNC",
                    "command": command,
                    "pid": process.pid,
                },
            )
            return process

        except Exception:
            logger.exception(
                f"Error launching asynchronous command: {command}",
                extra_data={"action": "RUN_ASYNC_FAIL"},
            )
            return None

    # --- System Diagnostics ---

    @staticmethod
    def get_system_diagnostics() -> Optional[Dict[str, Union[int, float]]]:
        """
        Retrieves fundamental system statistics (CPU, memory, disk) using psutil.
        These are high-level inputs for the Orchestrator (L4).
        """
        try:
            cpu = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            diagnostics = {
                "cpu_percent": cpu,
                "mem_total_gb": round(memory.total / (1024**3), 2),
                "mem_used_gb": round(memory.used / (1024**3), 2),
                "mem_percent": memory.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_percent": disk.percent,
                "uptime_seconds": int(psutil.boot_time()),
            }
            logger.debug(
                "Retrieved system diagnostics.",
                extra_data={"cpu_load": cpu, "mem_percent": memory.percent},
            )
            return diagnostics
        except Exception:
            logger.exception("Failed to retrieve system diagnostics.")
            return None

    @staticmethod
    def get_process_info(pid: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed stats for a specific running process by PID.
        """
        try:
            process = psutil.Process(pid)
            info = process.as_dict(
                attrs=[
                    "pid",
                    "name",
                    "status",
                    "cpu_percent",
                    "memory_info",
                    "create_time",
                    "cmdline",
                ]
            )

            # Convert memory info to a simpler structure
            if "memory_info" in info:
                info["memory_rss_mb"] = round(info["memory_info"].rss / (1024**2), 2)
                del info["memory_info"]

            logger.debug(
                f"Retrieved info for PID {pid}.",
                extra_data={"pid": pid, "status": info.get("status")},
            )
            return info
        except psutil.NoSuchProcess:
            logger.error(f"Process with PID {pid} not found.")
            return None
        except Exception:
            logger.exception(f"Failed to retrieve info for PID {pid}.")
            return None


# --- Example Usage (Not part of the class, for testing blueprint) ---
# if __name__ == '__main__':
#     # Sync Run Example
#     result = ProcessManagement.run_command_sync(["ls", "-lha"])
#     print(f"Sync Command Result:\nReturn Code: {result['return_code']}\nSTDOUT:\n{result['stdout']}")

#     # Async Run Example (WARNING: Requires separate monitoring/killing)
#     # process = ProcessManagement.run_command_async(["sleep", "10"])
#     # if process:
#     #     print(f"Launched PID: {process.pid}. Remember to terminate it later!")
#     #     # To terminate: process.terminate()

#     # Diagnostics Example
#     # diagnostics = ProcessManagement.get_system_diagnostics()
#     # print(f"\nSystem Diagnostics:\n{diagnostics}")
