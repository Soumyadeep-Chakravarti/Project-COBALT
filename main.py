import os
import shutil
import time
from typing import Any, Dict, List

# --- Initialize Global Logger FIRST ---
# This ensures all subsequent module imports can access the logger instantly.
from utils.structured_logger import LoggerManager

logger = LoggerManager.get_logger("COBALT_MAIN")

# --- Import Core Modules (L1, L3, L4) ---
# L1: The Foundation (Action tools)
from src.L1_foundation.dir_manipulation import DirManager
from src.L1_foundation.file_manipulation import FileManager
from src.L1_foundation.process_management import ProcessManager
from src.L3_guardian.config_manager import ConfigManager

# L3: The Guardian (Security and Trust)
from src.L3_guardian.integrity_manager import IntegrityManager
from src.L4_orchestrator.communication_engine import CommunicationEngine
from src.L4_orchestrator.dynamic_provisioner import DynamicProvisioner

# L4: The Orchestrator (Cognition and Interface)
from src.L4_orchestrator.plan_engine import PlanEngine


def initialize_system():
    """Performs necessary setup steps for COBALT."""
    print("--- COBALT AI: System Initialization ---")
    logger.info("Initializing COBALT system services.")

    # 1. Ensure required directories exist (L1)
    DirManager.create_directory("workspace", exist_ok=True)
    DirManager.create_directory("logs", exist_ok=True)

    # 2. Clean up previous simulation runs
    if os.path.exists("sim_component"):
        shutil.rmtree("sim_component")
        logger.warning("Cleaned up previous simulation directory 'sim_component'.")

    # 3. Apply initial configuration (L3)
    initial_config_path = "workspace/system_settings.ini"
    config_data = {"System": {"max_cpu_utilization": 90, "audit_level": "CRITICAL"}}
    ConfigManager.write_config(initial_config_path, config_data, format_type="ini")
    logger.info(f"Loaded initial configuration from {initial_config_path}.")

    print("Initialization Complete. COBALT is Active.")
    print("-" * 40)


def simulate_complex_request(user_request: str):
    """
    Simulates the full orchestration pipeline for a user request.
    1. Communication: Map Intent.
    2. Dynamic Provisioning: Create component.
    3. Integrity: Verify component code.
    4. Plan Engine: Create and execute plan.
    5. Communication: Report status.
    """
    task_id = "TASK-" + str(int(time.time() * 100))
    print(f"\n[USER] Request: {user_request}")
    logger.info(
        "Starting new user request pipeline.",
        extra_data={"task_id": task_id, "request": user_request},
    )

    # 1. COMMUNICATION: Map Intent (L4)
    intent = CommunicationEngine.map_intent(user_request)
    print(
        f"[COBALT] Intent Mapped: Action='{intent['action']}', Priority='{intent['priority']}'"
    )

    # 2. DYNAMIC PROVISIONING: Create a new Rust component (L4)
    CommunicationEngine.provide_proactive_update(
        task_id, 0.1, "Analyzing request and selecting optimal language (L4)."
    )

    provision_result = DynamicProvisioner.provision_component(
        task_description="I need a high-performance, memory-safe worker for a systems core task.",
        component_name="sim_component",
    )

    if not provision_result["success"]:
        print(f"[COBALT] Fatal Error: {provision_result['message']}")
        return

    component_path = provision_result["component_path"]
    main_file_path = os.path.join(component_path, "src", "main.rs")
    print(
        f"[COBALT] Success: Component '{component_path}' provisioned with **{provision_result['language']}** blueprint."
    )

    # 3. INTEGRITY CHECK: Verify the generated code (L3)
    CommunicationEngine.provide_proactive_update(
        task_id, 0.4, "Verifying integrity of generated code (L3 Guardian check)."
    )

    # Calculate and store the trusted hash (simulated)
    trusted_hash = IntegrityManager.calculate_file_checksum(main_file_path)
    if not trusted_hash:
        logger.error(f"Failed to calculate trusted hash for {main_file_path}.")
        return

    # Verify the file (should pass)
    if IntegrityManager.verify_file_checksum(main_file_path, trusted_hash):
        print(f"[COBALT] Integrity PASSED: Generated code is verified and trusted.")
    else:
        print("[COBALT] Integrity FAILED: **CRITICAL WARNING!** Halting process.")
        return

    # 4. PLAN ENGINE: Create and Execute Plan (L4)
    # The plan: Build the component, then run it.
    plan_steps = [
        {
            "desc": f"Run Rust build process for {component_path}",
            "tool": "process",
            "command": f"echo Simulating: cargo build --release",
        },
        {
            "desc": f"Execute the built worker process",
            "tool": "process",
            "command": f"echo Simulating: ./{component_path}/target/release/worker_process",
        },
        {
            "desc": f"Clean up temporary files",
            "tool": "dir",
            "command": f"echo Simulating: rm -rf {component_path}/target",
        },
    ]

    CommunicationEngine.provide_proactive_update(
        task_id, 0.6, "Plan generated. Beginning execution (L1/L4 orchestration)."
    )

    execution_success = True
    for step in plan_steps:
        result = PlanEngine.execute_step(task_id, step)
        if not result.get("success"):
            print(f"[COBALT] Execution Failure: Step '{step['desc']}' failed.")
            execution_success = False
            break
        # Simulate execution time
        time.sleep(0.5)

    # 5. COMMUNICATION: Final Report (L4)
    final_state = {
        "cpu_load": 40,
        "target_service": "sim_component",
        "error_found": not execution_success,
    }

    if execution_success:
        CommunicationEngine.provide_proactive_update(
            task_id, 1.0, "All plan steps executed successfully."
        )
        response = CommunicationEngine.generate_response(intent, final_state)
    else:
        response = CommunicationEngine.generate_response(
            {"action": "diagnose"}, final_state
        )

    print(f"\n[COBALT FINAL REPORT]\n{response}")
    print("-" * 40)


if __name__ == "__main__":
    # Initialize the entire COBALT environment
    initialize_system()

    # Run a complete simulation of a complex user task
    simulate_complex_request(
        "Please deploy a new memory-safe worker to handle the core systems logic."
    )
