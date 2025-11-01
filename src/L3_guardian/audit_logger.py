import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, List, Optional, Union

from utils.structured_logger import LoggerManager  # Assumed dependency

# --- Configuration Constants for the Audit Logger ---
# NOTE: In a final C++/Rust system, this path would be managed by the core OS service.
AUDIT_LOG_FILE = "/var/log/cobalt_audit.jsonl"
MAX_LOG_SIZE_MB = 10
MAX_LOG_COUNT = 5  # Retain up to 5 files (1 active + 4 backups)

# Initialize a separate, dedicated logger for the audit trail
# This logger ensures messages are written immediately and securely.
audit_logger = LoggerManager.get_logger(
    "AUDIT_LOGGER", level=logging.INFO, propagate=False
)


class AuditLogger:
    """
    Manages the secure logging, rotation, and retrieval of all COBALT actions.
    This module secures the central source of truth for all system operations.
    Focuses on Layer 3 control: Historical Context and Traceability.
    """

    @staticmethod
    def initialize_secure_handler() -> bool:
        """
        Sets up the RotatingFileHandler for the audit log to ensure
        logs are rotated and do not exhaust disk space.
        """
        try:
            # 1. Ensure the directory exists (simulating L1 dependency)
            log_dir = os.path.dirname(AUDIT_LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # 2. Define the log handler with rotation policy
            file_handler = RotatingFileHandler(
                AUDIT_LOG_FILE,
                maxBytes=MAX_LOG_SIZE_MB * 1024 * 1024,
                backupCount=MAX_LOG_COUNT - 1,
                encoding="utf-8",
            )

            # Use the structured JSON formatter provided by LoggerManager
            formatter = LoggerManager.get_formatter()
            file_handler.setFormatter(formatter)

            # 3. Attach the handler to the dedicated audit logger
            if not any(
                isinstance(h, RotatingFileHandler) for h in audit_logger.handlers
            ):
                audit_logger.addHandler(file_handler)
                # Prevent logging from bubbling up to the root handler
                audit_logger.propagate = False

            # Set a restrictive permission mask for the log file (e.g., read/write for owner only)
            # NOTE: This only works effectively on Unix-like systems.
            if os.path.exists(AUDIT_LOG_FILE):
                os.chmod(AUDIT_LOG_FILE, 0o600)

            audit_logger.info(
                "Secure audit logging initialized.",
                extra={"path": AUDIT_LOG_FILE, "action": "INIT"},
            )
            return True
        except Exception:
            # Critical failure: Audit logging cannot be established
            logging.exception(
                "CRITICAL FAILURE: Cannot initialize secure audit logger."
            )
            return False

    @staticmethod
    def log_event(
        message: str, event_type: str, context: Optional[Dict[str, Any]] = None
    ):
        """
        Records a specific event in the audit trail.
        This is the primary method used by L4: Orchestrator.

        Args:
            message: A human-readable summary of the event.
            event_type: A structured identifier (e.g., 'CONFIG_CHANGE', 'PROC_KILL', 'AUTH_FAIL').
            context: A dictionary of additional data (L1/L2 results, parameters).
        """
        # Ensure initialization has been run (safer to call before every use)
        if not AuditLogger.is_initialized():
            AuditLogger.initialize_secure_handler()

        extra_data = {
            "event_type": event_type,
            "context": context if context is not None else {},
        }

        # Log the event using the dedicated audit logger instance
        audit_logger.info(message, extra=extra_data)

    @staticmethod
    def is_initialized() -> bool:
        """
        Checks if the rotating file handler is already attached.
        """
        return any(isinstance(h, RotatingFileHandler) for h in audit_logger.handlers)

    @staticmethod
    def retrieve_audit_trail(lines: int = 100) -> List[str]:
        """
        Securely reads the last N lines of the current audit log file.

        Args:
            lines: The number of lines to retrieve from the end of the file.

        Returns:
            A list of the last N log entries (raw JSON lines).
        """
        if not os.path.exists(AUDIT_LOG_FILE):
            return ["Audit file not found."]

        try:
            # Simple, non-library tail function for efficiency
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                # Read all lines (inefficient for HUGE files, but simple for blueprint)
                all_lines = f.readlines()

            # Return the last N lines
            logger.info(
                "Retrieved audit trail snapshot.",
                extra={"count": len(all_lines[-lines:])},
            )
            return [line.strip() for line in all_lines[-lines:]]

        except PermissionError:
            logger.error(
                "Permission denied reading audit log file.",
                extra={"path": AUDIT_LOG_FILE},
            )
            return ["ERROR: Permission denied access to audit logs."]
        except Exception:
            logger.exception("Unexpected error during audit log retrieval.")
            return ["ERROR: Failed to read audit logs."]


# Mandatory call to initialize the secure logging handler immediately
AuditLogger.initialize_secure_handler()
