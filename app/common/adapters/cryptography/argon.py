"""Argon2 password hasher implementation.

This module provides a secure password hashing implementation using the Argon2
algorithm, the winner of the Password Hashing Competition (PHC). It provides
strong security against various attack vectors including GPU/FPGA attacks.
"""

from typing import Any, Dict, Optional

from passlib.context import CryptContext
from passlib.exc import InvalidHashError, MalformedHashError

from app.common.interfaces.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    """Password hasher implementation using the Argon2 algorithm.

    This implementation uses Passlib's Argon2 with secure defaults and
    support for parameter tuning.

    Example:
        >>> hasher = Argon2PasswordHasher()
        >>> hashed = hasher.hash("mypassword")
        >>> hasher.verify("mypassword", hashed)
        True
    """

    # Secure default parameters based on OWASP recommendations
    DEFAULT_PARAMS = {
        "time_cost": 3,  # Number of iterations
        "memory_cost": 64 * 1024,  # Memory usage in kibibytes
        "parallelism": 4,  # Parallel threads
        "salt_size": 16,  # Salt size in bytes
        "hash_len": 32,  # Hash length in bytes
    }

    def __init__(self, **kwargs):
        """Initialize the hasher with optional custom parameters.

        Args:
            **kwargs: Optional parameter overrides for Argon2.
        """
        params = {**self.DEFAULT_PARAMS, **kwargs}

        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__time_cost=params["time_cost"],
            argon2__memory_cost=params["memory_cost"],
            argon2__parallelism=params["parallelism"],
            argon2__salt_size=params["salt_size"],
            argon2__hash_len=params["hash_len"],
        )

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plain text password to verify.
            hashed_password: Previously hashed password.
            options: Optional verification parameters (unused for Argon2).

        Returns:
            True if password matches, False otherwise.

        Note:
            Uses constant-time comparison to prevent timing attacks.
        """
        if not plain_password or not hashed_password:
            raise ValueError("Password and hash must not be empty")

        return self.pwd_context.verify(plain_password, hashed_password)

    def hash(self, password: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Hash a password using Argon2.

        Args:
            password: Plain text password to hash.
            options: Optional hashing parameters.

        Returns:
            PHC-formatted Argon2 hash string.

        Raises:
            ValueError: If password is invalid.

        Note:
            Hash string includes algorithm parameters and salt.
        """
        if not password:
            raise ValueError("Password must not be empty")

        try:
            return self.pwd_context.hash(
                password, **({} if options is None else options)
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Password hashing failed: {str(e)}")

    def needs_rehash(
        self, hashed_password: str, options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if password needs rehashing.

        Args:
            hashed_password: Existing hash to check.
            options: Optional parameters to compare against.

        Returns:
            True if hash uses different parameters than current config.

        Raises:
            ValueError: If hash format is invalid.
        """
        try:
            return self.pwd_context.needs_update(hashed_password)
        except ValueError as e:
            raise ValueError(f"Invalid hash format: {str(e)}")

    @property
    def algorithm(self) -> str:
        """Get the hashing algorithm name.

        Returns:
            "argon2id" (current Argon2 version).
        """
        return "argon2id"

    def get_parameters(self, hashed_password: str) -> Dict[str, Any]:
        """Extract parameters from a hash string.

        Args:
            hashed_password: Hash to analyze.

        Returns:
            Dictionary of Argon2 parameters used.

        Raises:
            ValueError: If hash format is invalid.
        """
        try:
            hash_obj = self.pwd_context.handler().from_string(hashed_password)
            return {
                "time_cost": hash_obj.time_cost,
                "memory_cost": hash_obj.memory_cost,
                "parallelism": hash_obj.parallelism,
                "salt_size": len(hash_obj.salt),
                "hash_len": len(hash_obj.checksum),
            }
        except (InvalidHashError, MalformedHashError) as e:
            raise ValueError(f"Invalid hash format: {str(e)}")
