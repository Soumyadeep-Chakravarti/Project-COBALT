import csv
import json
import mimetypes
import os
from typing import IO, Any, Dict, Generator, List, Optional, Union

from utils.structured_logger import LoggerManager

# Initialize the logger for this specific module
logger = LoggerManager.get_logger("FILE_MANIPULATION")


class FileManipulation:
    """
    Provides robust, atomic, and safe file I/O operations across all major data types.
    Focuses on Layer 1 control: Data and Content.
    """

    # --- Utility and Metadata Methods ---

    @staticmethod
    def get_stats(filepath: str) -> Optional[Dict[str, Union[int, float, str]]]:
        """
        Retrieves basic filesystem statistics for a file (size, creation time, MIME type).

        Args:
            filepath: The path to the file.

        Returns:
            A dictionary of stats, or None on failure.
        """
        try:
            stat_result = os.stat(filepath)
            mime_type, _ = mimetypes.guess_type(filepath)

            stats = {
                "size_bytes": stat_result.st_size,
                "created_time_ts": stat_result.st_ctime,
                "modified_time_ts": stat_result.st_mtime,
                "mime_type": mime_type if mime_type else "application/octet-stream",
                "is_file": os.path.isfile(filepath),
            }
            logger.debug(f"Retrieved stats for: {filepath}")
            return stats
        except FileNotFoundError:
            logger.error(f"Cannot retrieve stats: File not found at {filepath}")
            return None
        except Exception:
            logger.exception(f"Unexpected error retrieving stats for {filepath}")
            return None

    # --- Text/Standard I/O ---

    @staticmethod
    def read_text(filepath: str) -> Optional[str]:
        """Reads the entire content of a file as a string."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(
                f"Successfully read text file: {filepath}",
                extra_data={"size": len(content), "mode": "text"},
            )
            return content
        except FileNotFoundError:
            logger.error(f"Text file not found: {filepath}")
            return None
        except Exception:
            logger.exception(f"Error reading text file: {filepath}")
            return None

    @staticmethod
    def write_text(filepath: str, content: str, overwrite: bool = True) -> bool:
        """Writes content to a file, optionally preventing overwrite."""
        if not overwrite and os.path.exists(filepath):
            logger.error(
                f"File exists and overwrite is False: {filepath}",
                extra_data={"action": "WRITE_FAIL"},
            )
            return False

        try:
            mode = (
                "w" if overwrite else "a"
            )  # Use 'w' mode, 'a' for append not write (but safety check covers it)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(
                f"Successfully wrote text file: {filepath}",
                extra_data={"size": len(content), "mode": "text_write"},
            )
            return True
        except Exception:
            logger.exception(f"Error writing text file: {filepath}")
            return False

    # --- Structured I/O (JSON and CSV) ---

    @staticmethod
    def read_json(filepath: str) -> Optional[Dict[str, Any]]:
        """Reads and deserializes a JSON file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(
                f"Successfully read and parsed JSON file: {filepath}",
                extra_data={"mode": "json_read"},
            )
            return data
        except FileNotFoundError:
            logger.error(f"JSON file not found: {filepath}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in file: {filepath}")
            return None
        except Exception:
            logger.exception(f"Error reading JSON file: {filepath}")
            return None

    @staticmethod
    def write_json(filepath: str, data: Dict[str, Any]) -> bool:
        """Serializes and writes data to a JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info(
                f"Successfully wrote JSON file: {filepath}",
                extra_data={"mode": "json_write"},
            )
            return True
        except Exception:
            logger.exception(f"Error writing JSON file: {filepath}")
            return False

    @staticmethod
    def read_csv(filepath: str, delimiter: str = ",") -> Optional[List[Dict[str, str]]]:
        """Reads and returns the content of a CSV file as a list of dictionaries."""
        try:
            with open(filepath, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                data = list(reader)
            logger.info(
                f"Successfully read CSV file: {filepath}",
                extra_data={"rows": len(data), "mode": "csv_read"},
            )
            return data
        except FileNotFoundError:
            logger.error(f"CSV file not found: {filepath}")
            return None
        except Exception:
            logger.exception(f"Error reading CSV file: {filepath}")
            return None

    @staticmethod
    def write_csv(
        filepath: str, data: List[Dict[str, Any]], delimiter: str = ","
    ) -> bool:
        """Writes a list of dictionaries to a CSV file."""
        if not data:
            logger.warning(f"Attempted to write empty list to CSV: {filepath}")
            return False

        try:
            fieldnames = list(data[0].keys())
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            logger.info(
                f"Successfully wrote CSV file: {filepath}",
                extra_data={"rows": len(data), "mode": "csv_write"},
            )
            return True
        except Exception:
            logger.exception(f"Error writing CSV file: {filepath}")
            return False

    # --- Binary and Streaming I/O ---

    @staticmethod
    def read_binary(filepath: str) -> Optional[bytes]:
        """Reads the entire content of a file as raw bytes."""
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            logger.info(
                f"Successfully read binary file: {filepath}",
                extra_data={"size": len(content), "mode": "binary_read"},
            )
            return content
        except FileNotFoundError:
            logger.error(f"Binary file not found: {filepath}")
            return None
        except Exception:
            logger.exception(f"Error reading binary file: {filepath}")
            return None

    @staticmethod
    def write_binary(filepath: str, content: bytes) -> bool:
        """Writes raw bytes to a file."""
        try:
            with open(filepath, "wb") as f:
                f.write(content)
            logger.info(
                f"Successfully wrote binary file: {filepath}",
                extra_data={"size": len(content), "mode": "binary_write"},
            )
            return True
        except Exception:
            logger.exception(f"Error writing binary file: {filepath}")
            return False

    @staticmethod
    def read_stream(
        filepath: str, chunk_size: int = 4096
    ) -> Optional[Generator[bytes, None, None]]:
        """
        Reads a file in chunks for memory-efficient processing (streaming).
        Returns a generator of bytes.
        """
        if not os.path.exists(filepath):
            logger.error(f"File for streaming not found: {filepath}")
            return None

        def file_generator(path: str):
            try:
                with open(path, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
                logger.info(
                    f"Successfully completed streaming read: {path}",
                    extra_data={"mode": "stream_read"},
                )
            except Exception:
                logger.exception(f"Error during file streaming: {path}")

        return file_generator(filepath)
