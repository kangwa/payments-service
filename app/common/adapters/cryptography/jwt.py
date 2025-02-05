"""JWT implementation of token management interface.

This module provides a JWT-based implementation of the TokenManager interface
using the PyJWT library for token operations.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt

from app.common.exceptions import ExpiredTokenError, InvalidTokenError, TokenError
from app.common.interfaces.token_manager import TokenManager


class JWTManager(TokenManager):
    """JWT token manager for authentication and authorization.

    Implements the TokenManager interface using JSON Web Tokens (JWT).
    Handles token creation, encoding, and validation using the PyJWT library.

    Args:
        secret_key: Secret key for token signing and verification.
        algorithm: JWT algorithm to use (default: HS256).

    Example:
        >>> manager = JWTManager("secret-key", algorithm="HS256")
        >>> token = manager.create_access_token({"user_id": "123"})
    """

    DEFAULT_EXPIRE_MINUTES: int = 15

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a new JWT access token.

        Args:
            data: Dictionary of claims to include in token.
            expires_delta: Optional custom expiration time.

        Returns:
            Encoded JWT token string.

        Raises:
            TokenError: If token creation fails.
        """
        try:
            to_encode = data.copy()
            expire = datetime.now() + (
                expires_delta
                if expires_delta
                else timedelta(minutes=self.DEFAULT_EXPIRE_MINUTES)
            )
            to_encode.update({"exp": expire})
            return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            raise TokenError(f"Token creation failed: {str(e)}")

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token.

        Args:
            token: JWT token string to decode.

        Returns:
            Dictionary of decoded token claims.

        Raises:
            ExpiredTokenError: If token has expired.
            InvalidTokenError: If token is malformed.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")

    def refresh_token(
        self, token: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create new token with extended expiration.

        Args:
            token: Existing valid token to refresh.
            expires_delta: Optional new expiration time.

        Returns:
            New token with extended validity.

        Raises:
            TokenError: If refresh fails.
        """
        try:
            payload = self.decode_token(token)
            # Remove old expiration
            del payload["exp"]
            return self.create_access_token(payload, expires_delta)
        except (ExpiredTokenError, InvalidTokenError) as e:
            raise TokenError(f"Cannot refresh invalid token: {str(e)}")

    def verify_token(self, token: str) -> bool:
        """Verify token validity without full decode.

        Args:
            token: Token string to verify.

        Returns:
            True if token is valid, False otherwise.
        """
        try:
            # Verify signature and expiration only
            jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": True},
            )
            return True
        except jwt.InvalidTokenError:
            return False

    @property
    def default_expiration(self) -> timedelta:
        """Get default token expiration time.

        Returns:
            Default expiration duration.
        """
        return timedelta(minutes=self.DEFAULT_EXPIRE_MINUTES)
