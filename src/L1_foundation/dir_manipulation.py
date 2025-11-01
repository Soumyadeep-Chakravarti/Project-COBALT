import os
import shutil
from typing import Dict, Optional, Union

# Assuming the utility is in utils/structured_logger.py
from utils.structured_logger import LoggerManager

# Initialize the logger for this specific module
logger = LoggerManager.get_logger("DIR_MANIPULATION")


class DirManipulation:
    """
    Provides robust, atomic, and safe directory management operations.
    Focuses on Layer 1 control: Volume and Structure.

    All operations log their success or failure for the Audit Layer (L3).
    """

    @staticmethod
    def create_directory(path: str, exist_ok: bool = True) -> bool:
        """
        Creates a directory and any necessary parent directories.

        Args:
            path: The directory path to create.
            exist_ok: If False, raises FileExistsError if the directory already exists.

        Returns:
            True if creation was successful or directory already exists (and exist_ok=True), False otherwise.
        """
        try:
            os.makedirs(path, exist_ok=exist_ok)
            logger.info(
                f"Directory created or verified: {path}",
                extra_data={"action": "CREATE"},
            )
            return True
        except FileExistsError:
            # Only hit if exist_ok is False
            logger.error(
                f"Directory already exists and exist_ok=False: {path}",
                extra_data={"action": "CREATE_FAIL"},
            )
            return False
        except PermissionError:
            logger.error(
                f"Permission denied creating directory: {path}",
                extra_data={"action": "CREATE_FAIL"},
            )
            return False
        except Exception:
            logger.exception(
                f"Unexpected error creating directory: {path}",
                extra_data={"action": "CREATE_FAIL"},
            )
            return False

    @staticmethod
    def remove_directory(path: str, recursive: bool = False) -> bool:
        """
        Removes a directory. Can be non-recursive (os.rmdir) or recursive (shutil.rmtree).

        Args:
            path: The directory path to remove.
            recursive: If True, remove directory and all its contents (DANGER: ATOMIC OPERATION).

        Returns:
            True if removal was successful, False otherwise.
        """
        if not os.path.exists(path):
            logger.warning(
                f"Attempted removal of non-existent directory: {path}",
                extra_data={"action": "REMOVE_SKIP"},
            )
            return True

        try:
            if recursive:
                # DANGER ZONE: Remove contents recursively (like 'rm -rf')
                shutil.rmtree(path)
                logger.info(
                    f"Directory and contents recursively removed: {path}",
                    extra_data={"action": "REMOVE_RECURSIVE"},
                )
            else:
                # Safe operation: remove only if empty
                os.rmdir(path)
                logger.info(
                    f"Empty directory removed: {path}",
                    extra_data={"action": "REMOVE_EMPTY"},
                )
            return True
        except NotADirectoryError:
            logger.error(
                f"Path is a file, not a directory: {path}",
                extra_data={"action": "REMOVE_FAIL"},
            )
            return False
        except OSError as e:
            if not recursive and "Directory not empty" in str(e):
                logger.error(
                    f"Directory not empty. Use recursive=True to force removal: {path}.",
                    extra_data={"action": "REMOVE_FAIL"},
                )
            else:
                logger.exception(
                    f"OS error during directory removal: {path}",
                    extra_data={"action": "REMOVE_FAIL"},
                )
            return False
        except Exception:
            logger.exception(
                f"Unexpected error removing directory: {path}",
                extra_data={"action": "REMOVE_FAIL"},
            )
            return False

    @staticmethod
    def list_contents(path: str, full_path: bool = False) -> Optional[list[str]]:
        """
        Lists all files and directories inside a given path.

        Args:
            path: The directory path to inspect.
            full_path: If True, returns full absolute paths instead of just names.

        Returns:
            A list of content names/paths, or None on failure.
        """
        try:
            contents = os.listdir(path)
            if full_path:
                contents = [os.path.join(path, item) for item in contents]

            logger.info(
                f"Listed contents of directory: {path}",
                extra_data={"count": len(contents)},
            )
            return contents
        except FileNotFoundError:
            logger.error(f"Cannot list contents: Directory not found at {path}")
            return None
        except PermissionError:
            logger.error(f"Cannot list contents: Permission denied for {path}")
            return None
        except Exception:
            logger.exception(f"Unexpected error listing contents of {path}")
            return None

    @staticmethod
    def get_stats(path: str) -> Optional[Dict[str, Union[int, float]]]:
        """
        Retrieves basic filesystem statistics for a path.

        Args:
            path: The directory path to inspect.

        Returns:
            A dictionary of stats, or None on failure.
        """
        try:
            stat_result = os.stat(path)
            stats = {
                "size_bytes": stat_result.st_size,
                "created_time_ts": stat_result.st_ctime,
                "modified_time_ts": stat_result.st_mtime,
                "is_directory": os.path.isdir(path),
            }
            logger.debug(f"Retrieved stats for: {path}")
            return stats
        except FileNotFoundError:
            logger.error(f"Cannot retrieve stats: Path not found at {path}")
            return None
        except Exception:
            logger.exception(f"Unexpected error retrieving stats for {path}")
            return None
