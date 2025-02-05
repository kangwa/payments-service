"""Token management interface for authentication.

This module defines the abstract interface for token management operations,
providing a consistent contract for different token implementations (JWT, etc.).
"""

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Dict, Optional


class TokenManager(ABC):
    """Abstract interface for authentication token management.

    This interface defines the contract for token management implementations,
    providing methods for creating and validating authentication tokens.
    Implementations should handle token generation, validation, and encoding
    according to their specific token format (e.g., JWT, OAuth).

    Example:
        >>> token_manager = JWTTokenManager(secret_key="secret", algorithm="HS256")
        >>> token = token_manager.create_access_token(
        ...     data={"user_id": "123"},
        ...     expires_delta=timedelta(minutes=30)
        ... )
        >>> payload = token_manager.decode_token(token)
    """

    @abstractmethod
    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create an access token with the given payload and expiration.

        Args:
            data: Dictionary containing the token payload.
            expires_delta: Optional token validity duration. If not provided,
                implementation should use a reasonable default.

        Returns:
            Encoded token string.

        Raises:
            TokenError: If token creation fails.

        Example:
            >>> token = token_manager.create_access_token(
            ...     data={"user_id": "123", "email": "user@example.com"},
            ...     expires_delta=timedelta(hours=1)
            ... )
        """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a token.

        Args:
            token: The token string to decode and validate.

        Returns:
            Dictionary containing the decoded token payload.

        Raises:
            TokenError: If token is invalid, expired, or malformed.

        Example:
            >>> try:
            ...     payload = token_manager.decode_token(token)
            ...     user_id = payload.get("user_id")
            ... except TokenError as e:
            ...     # Handle invalid token
            ...     pass
        """
        pass

    @abstractmethod
    def refresh_token(
        self, token: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a new token extending the validity period.

        Args:
            token: Existing valid token to refresh.
            expires_delta: Optional new validity duration. If not provided,
                implementation should use a reasonable default.

        Returns:
            New token string with extended validity.

        Raises:
            TokenError: If token refresh fails or original token is invalid.

        Example:
            >>> new_token = token_manager.refresh_token(
            ...     old_token,
            ...     expires_delta=timedelta(days=7)
            ... )
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> bool:
        """Verify if a token is valid without decoding it.

        This method should perform a lightweight validation of the token
        format and signature without fully decoding the payload.

        Args:
            token: The token string to verify.

        Returns:
            True if token is valid, False otherwise.

        Example:
            >>> if token_manager.verify_token(token):
            ...     payload = token_manager.decode_token(token)
        """
        pass
