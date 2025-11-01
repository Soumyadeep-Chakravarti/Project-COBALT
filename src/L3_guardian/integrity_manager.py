import hashlib
import os
from typing import Optional, Union

from utils.structured_logger import LoggerManager

# Initialize the logger for this security module
logger = LoggerManager.get_logger("INTEGRITY_MANAGER")

# Define the standard algorithm for COBALT's integrity checks
STANDARD_HASH_ALGO = "sha256"


class IntegrityManager:
    """
    Manages the verification of file and data integrity using cryptographic hashing.
    Ensures data trust across all L1 and L2 operations before execution.
    Focuses on Layer 3 control: Data Trust and Pre-Execution Validation.
    """

    @staticmethod
    def calculate_checksum(
        data: Union[str, bytes], algorithm: str = STANDARD_HASH_ALGO
    ) -> Optional[str]:
        """
        Calculates the cryptographic checksum of a string or bytes object.

        Args:
            data: The input string or bytes to hash.
            algorithm: The hashing algorithm to use (e.g., 'sha256', 'sha3_256').

        Returns:
            The hexadecimal checksum string, or None on error.
        """
        try:
            hasher = hashlib.new(algorithm)
            if isinstance(data, str):
                data = data.encode("utf-8")
            hasher.update(data)
            checksum = hasher.hexdigest()
            logger.debug(
                f"Calculated checksum for in-memory data.",
                extra_data={"algorithm": algorithm, "checksum_start": checksum[:8]},
            )
            return checksum
        except ValueError:
            logger.error(
                f"Unsupported hashing algorithm: {algorithm}",
                extra_data={"algorithm": algorithm},
            )
            return None
        except Exception:
            logger.exception("Unexpected error calculating checksum for data.")
            return None

    @staticmethod
    def calculate_file_checksum(
        filepath: str, algorithm: str = STANDARD_HASH_ALGO
    ) -> Optional[str]:
        """
        Calculates the checksum of a file, reading it in chunks to handle
        large files without exhausting memory.

        Args:
            filepath: The path to the file on the filesystem.
            algorithm: The hashing algorithm to use.

        Returns:
            The hexadecimal checksum string, or None on error.
        """
        if not os.path.exists(filepath):
            logger.warning(
                f"File not found for checksum calculation.",
                extra_data={"filepath": filepath},
            )
            return None

        try:
            hasher = hashlib.new(algorithm)
            # Read in 64KB chunks
            block_size = 65536
            with open(filepath, "rb") as f:
                while True:
                    data = f.read(block_size)
                    if not data:
                        break
                    hasher.update(data)

            checksum = hasher.hexdigest()
            logger.info(
                f"File checksum calculated.",
                extra_data={"filepath": filepath, "checksum_start": checksum[:8]},
            )
            return checksum
        except ValueError:
            logger.error(
                f"Unsupported hashing algorithm: {algorithm}",
                extra_data={"algorithm": algorithm},
            )
            return None
        except Exception:
            logger.exception(f"Error calculating file checksum for {filepath}")
            return None

    @staticmethod
    def verify_file_checksum(
        filepath: str, expected_checksum: str, algorithm: str = STANDARD_HASH_ALGO
    ) -> bool:
        """
        Calculates a file's checksum and compares it against an expected value.

        Args:
            filepath: The path to the file.
            expected_checksum: The known, trusted checksum string.
            algorithm: The hashing algorithm to use.

        Returns:
            True if the calculated checksum matches the expected checksum, False otherwise.
        """
        calculated_checksum = IntegrityManager.calculate_file_checksum(
            filepath, algorithm
        )

        if calculated_checksum is None:
            # Error was already logged by the calculation function
            return False

        is_valid = calculated_checksum.lower() == expected_checksum.lower()

        if is_valid:
            logger.info(
                "Integrity check PASSED.",
                extra_data={"filepath": filepath, "check": "PASS"},
            )
        else:
            logger.critical(
                "Integrity check FAILED: File corruption detected.",
                extra_data={
                    "filepath": filepath,
                    "expected": expected_checksum[:8],
                    "actual": calculated_checksum[:8],
                    "check": "FAIL",
                },
            )

        return is_valid
