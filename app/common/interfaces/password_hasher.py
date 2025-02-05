"""Password hashing interface for secure password management.

This module defines the abstract interface for password hashing operations,
ensuring consistent and secure password handling across different hashing
implementations (e.g., bcrypt, argon2, PBKDF2).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class PasswordHasher(ABC):
    """Abstract interface for password hashing operations.

    This interface defines the contract for password hashing implementations,
    providing methods for secure password hashing and verification while
    supporting configurable hashing parameters.

    Example:
        >>> hasher = Argon2PasswordHasher()
        >>> hashed = hasher.hash("mypassword")
        >>> hasher.verify("mypassword", hashed)
        True
    """

    @abstractmethod
    def verify(
        self,
        plain_password: str,
        hashed_password: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Verify if a plain password matches its hashed version.

        Args:
            plain_password: Plain text password to verify.
            hashed_password: Hashed password to compare against.
            options: Optional verification parameters (e.g., pepper).

        Returns:
            True if password matches, False otherwise.

        Raises:
            ValueError: If passwords are invalid or in wrong format.

        Example:
            >>> is_valid = hasher.verify(
            ...     plain_password="mypassword",
            ...     hashed_password="$argon2id$v=19$...",
            ...     options={"pepper": "app-specific-key"}
            ... )
        """
        pass

    @abstractmethod
    def hash(self, password: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Hash a plain text password securely.

        Args:
            password: Plain text password to hash.
            options: Optional hashing parameters (e.g., salt, rounds).

        Returns:
            Securely hashed password string.

        Raises:
            ValueError: If password is invalid or options are incorrect.

        Example:
            >>> hashed = hasher.hash(
            ...     password="mypassword",
            ...     options={
            ...         "salt": "random-salt",
            ...         "rounds": 12
            ...     }
            ... )
        """
        pass

    @abstractmethod
    def needs_rehash(
        self, hashed_password: str, options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if password needs to be rehashed.

        Determines if the password hash was created using different parameters
        than currently configured (e.g., different number of rounds).

        Args:
            hashed_password: Previously hashed password to check.
            options: Optional parameters to compare against.

        Returns:
            True if password should be rehashed, False otherwise.

        Example:
            >>> if hasher.needs_rehash(user.password):
            ...     user.password = hasher.hash(plain_password)
        """
        pass

    @property
    @abstractmethod
    def algorithm(self) -> str:
        """Get the name of the hashing algorithm.

        Returns:
            Algorithm identifier string (e.g., "argon2id", "bcrypt").
        """
        pass

    @abstractmethod
    def get_parameters(self, hashed_password: str) -> Dict[str, Any]:
        """Extract hashing parameters from a hashed password.

        Args:
            hashed_password: Hashed password to analyze.

        Returns:
            Dictionary of parameters used for this hash.

        Raises:
            ValueError: If password hash format is invalid.

        Example:
            >>> params = hasher.get_parameters(hashed_password)
            >>> print(f"Hash uses {params['rounds']} rounds")
        """
        pass
