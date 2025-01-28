from abc import ABC, abstractmethod
from app.core.auth.models import User


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
