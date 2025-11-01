import datetime
import json
import logging
from typing import Any, Dict

# --- Structured Logging Setup for COBALT ---


class StructuredFormatter(logging.Formatter):
    """
    A custom formatter that outputs log records as structured JSON,
    ensuring machine-readability for the Audit Logger (Layer 3).
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "file_line": f"{record.filename}:{record.lineno}",
            "proc_id": record.process,
            "thread_id": record.thread,
        }

        # Add exception/traceback info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Ensure 'extra' data attached by the user is included
        log_record.update(record.__dict__.get("extra_data", {}))

        return json.dumps(log_record)


class LoggerManager:
    """
    Manages the creation and retrieval of configured loggers for COBALT modules.
    All modules should call LoggerManager.get_logger(__name__).
    """

    LOG_LEVEL = logging.INFO
    LOG_FILE = "cobalt_audit.log"

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Retrieves or creates a configured logger instance."""
        logger = logging.getLogger(name)
        if logger.hasHandlers():
            return logger

        logger.setLevel(LoggerManager.LOG_LEVEL)

        # 1. Console Handler (for real-time feedback)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())
        logger.addHandler(console_handler)

        # 2. File Handler (for the persistent Audit Log)
        file_handler = logging.FileHandler(LoggerManager.LOG_FILE)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

        return logger


# Initialize the root logger to catch any unhandled log events
LoggerManager.get_logger("COBALT_ROOT")
