# L05: Model Layer / Data Contracts

## Purpose
This layer defines the canonical, strict data schemas (Pydantic models) used for communication across **all** COBALT layers. It serves as the single source of truth for inter-layer data transfer, enforcing type safety and structural integrity essential for polyglot systems.

## Key Components

### 1. ExecutionCommand (Input to L02)
Defines all parameters required to execute a single shell command.
| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `command` | `str` | The executable path or name. | `"git"` |
| `args` | `List[str]` | List of arguments to pass. | `["status", "-s"]` |
| `cwd` | `Optional[str]` | The working directory. | `/home/user/project` |
| `timeout` | `float` | Max execution time in seconds. | `300.0` |
| `env_vars` | `Dict[str, str]` | Environment variables to override. | `{"DEBUG": "1"}` |
| `context_id` | `str` | Unique ID for tracking this specific execution. | `TASK_DEPLOY_BUILD` |

### 2. ExecutionResult (Output from L02)
Defines the standard, immutable result of a single command execution.
| Field | Type | Description | Notes |
| :--- | :--- | :--- | :--- |
| `status` | `Literal` | `SUCCESS`, `FAILURE`, `TIMEOUT`, or `ERROR`. | The final outcome state. |
| `exit_code` | `int` | OS return code. `-1` if unavailable. | |
| `duration_s` | `float` | Total execution time. | |
| `stdout` | `str` | Captured standard output. | |
| `stderr` | `str` | Captured standard error. | |
| `error_message` | `Optional[str]` | Detailed message on non-SUCCESS status. | |
