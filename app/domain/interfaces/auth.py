from abc import ABC, abstractmethod
from app.domain.models.auth import User


class PasswordHasher(ABC):
    """Abstract interface for password hashing operations.

    This interface defines the contract for password hashing implementations,
    providing methods for both hashing and verification of passwords.
    """

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify if a plain password matches its hashed version.

        Args:
            plain_password: The password in plain text to verify
            hashed_password: The hashed password to compare against

        Returns:
            bool: True if the password matches, False otherwise
        """
        pass

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain text password.

        Args:
            password: The plain text password to hash

        Returns:
            str: The hashed password
        """
        pass


class TokenManager(ABC):
    """Abstract interface for JWT token management.

    This interface defines the contract for token management implementations,
    providing methods for creating and decoding authentication tokens.
    """

    @abstractmethod
    def create_access_token(self, user: User) -> str:
        """Create an access token for a user.

        Args:
            user: The user to create the token for

        Returns:
            str: The generated access token
        """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode and validate a token.

        Args:
            token: The token to decode and validate

        Returns:
            dict: The decoded token payload

        Raises:
            ValueError: If the token is invalid or expired
        """
        pass
