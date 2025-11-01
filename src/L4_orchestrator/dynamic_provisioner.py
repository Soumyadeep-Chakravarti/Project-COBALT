import os
import uuid
from typing import Any, Dict, List, Optional

from src.L1_foundation.dir_manipulation import DirManager
from src.L1_foundation.file_manipulation import FileManager
from utils.structured_logger import LoggerManager

logger = LoggerManager.get_logger("DYNAMIC_PROVISIONER")


class DynamicProvisioner:
    """
    Manages the autonomous selection of the appropriate language (from the 9-language stack)
    and generates initial code, configuration, or boilerplate scripts.
    This enables COBALT's self-extending and polyglot capabilities.
    Focuses on Layer 4 control: Dynamic Tool Creation.
    """

    # Blueprint mapping of the 9-Language Stack to their primary purpose,
    # used by the provisioner to make selection decisions.
    LANGUAGE_ROLES: Dict[str, str] = {
        "rust": "Secure Systems Core/High-Performance Worker",
        "c": "Bare-Metal Interface/FFI Bridge",
        "go": "Networking/Microservice Orchestration",
        "java": "Enterprise Stability/Transactional Backend",
        "python": "AI/ML Model Serving/Automation Scripting",
        "elixir": "Fault Tolerance/Real-time Concurrency",
        "haskell": "Functional Verification/Core State Logic",
        "julia": "High-Speed Numerical Computing",
        "lua": "Embedded Scripting/Hot-Swappable Logic",
    }

    @staticmethod
    def _select_language(task_description: str) -> Optional[str]:
        """
        Simulates the cognitive choice of the best language for a task.
        In the full system, this would be an LLM decision; here, we use keyword matching.
        """
        task = task_description.lower()

        if "numerical" in task or "array" in task or "matrix" in task:
            return "julia"
        if (
            "real-time" in task
            or "concurrent connections" in task
            or "fault-tolerance" in task
        ):
            return "elixir"
        if "api gateway" in task or "concurrent i/o" in task or "network" in task:
            return "go"
        if "security" in task or "memory safe" in task or "systems core" in task:
            return "rust"
        if "ai" in task or "model" in task or "script" in task:
            return "python"

        # Default to a safe, general-purpose choice if keywords are ambiguous
        return "python"

    @staticmethod
    def _generate_boilerplate(language: str, component_name: str) -> Dict[str, str]:
        """
        Generates the basic files (code + config) required for a new component.
        """
        if language == "rust":
            return {
                f"{component_name}/Cargo.toml": f'[package]\nname = "{component_name}"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\ntokio = {{ version = "1", features = ["full"] }}',
                f"{component_name}/src/main.rs": f'// Rust Secure Worker: {component_name}\nfn main() {{\n    println!("Rust worker initialized for role: Secure Systems Core");\n}}',
            }
        elif language == "go":
            return {
                f"{component_name}/go.mod": f"module {component_name}\n\ngo 1.20\n\nrequire (\n\tgithup.com/gorilla/mux v1.8.0\n)",
                f"{component_name}/main.go": f'// Go API Gateway: {component_name}\npackage main\n\nimport "fmt"\n\nfunc main() {{\n\tfmt.Println("Go service ready for network orchestration.")\n}}',
            }
        elif language == "lua":
            return {
                f"{component_name}/script.lua": f'-- Lua Embedded Script: {component_name}\nfunction run_logic(data)\n    print("Running minimal, hot-swappable logic.")\n    return data\nend',
            }
        elif language == "python":
            return {
                f"{component_name}/requirements.txt": "tensorflow==2.10.0\nnumpy==1.23.5",
                f"{component_name}/service.py": f"# Python ML Service: {component_name}\nimport numpy as np\n# AI/ML Model serving logic goes here",
            }
        # Fallback case
        return {
            f"{component_name}/README.txt": f"Boilerplate not yet defined for {language}."
        }

    @staticmethod
    def provision_component(
        task_description: str, component_name: Optional[str] = None
    ) -> Dict[str, Union[str, bool]]:
        """
        Main entry point for autonomous component provisioning.

        Args:
            task_description: The user request or plan step defining the required tool.
            component_name: Optional, preferred name for the new component.

        Returns:
            A status dictionary detailing the outcome.
        """
        component_name = (
            component_name if component_name else f"comp-{str(uuid.uuid4())[:8]}"
        )
        language = DynamicProvisioner._select_language(task_description)

        if not language:
            return {
                "success": False,
                "message": "Could not determine appropriate language for the task.",
            }

        logger.info(
            f"Provisioning new component '{component_name}' using selected language: {language}.",
            extra_data={
                "language_role": DynamicProvisioner.LANGUAGE_ROLES.get(
                    language, "Unknown"
                ),
                "language": language,
            },
        )

        # 1. Generate the files (Blueprint L4)
        file_map = DynamicProvisioner._generate_boilerplate(language, component_name)

        # 2. Create the root directory (L1 Dir Manipulation)
        DirManager.create_directory(component_name)

        # 3. Write all boilerplate files (L1 File Manipulation)
        files_written = 0
        for filepath, content in file_map.items():
            if FileManager.write_file(filepath, content):
                files_written += 1
            else:
                logger.error(
                    f"Failed to write boilerplate file: {filepath}",
                    extra_data={"component": component_name},
                )

        if files_written == len(file_map):
            return {
                "success": True,
                "language": language,
                "component_path": component_name,
                "message": f"Successfully provisioned {language} component: {component_name}",
            }
        else:
            return {
                "success": False,
                "message": f"Partial failure: Only {files_written}/{len(file_map)} files written.",
            }


# --- Example Usage (Not part of the class, for testing blueprint) ---
# if __name__ == '__main__':
#     # 1. Provision a Rust security worker
#     rust_task = "I need a high-performance, memory-safe systems core worker."
#     rust_result = DynamicProvisioner.provision_component(rust_task, "trust_monitor")
#     print(f"Rust Provisioning Result: {rust_result}")

#     # 2. Provision a Julia matrix operation script
#     julia_task = "Calculate the inverse of a 1000x1000 matrix using high-speed numerical computing."
#     julia_result = DynamicProvisioner.provision_component(julia_task, "matrix_solver")
#     print(f"Julia Provisioning Result: {julia_result}")
