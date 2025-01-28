from uuid import UUID
import jwt
from datetime import datetime, timedelta
from typing import Optional

from app.core.auth.exceptions import ExpiredTokenError, InvalidTokenError
from app.core.auth.interfaces.password_hasher_interface import TokenManager
from app.core.auth.models.token_data_model import TokenData


class JWTManager(TokenManager):
    """JWT token manager for authentication and authorization.

    Implements the TokenManager interface using JSON Web Tokens (JWT).
    Handles token creation, encoding, and validation using the PyJWT library.

    Attributes:
        secret_key (str): Secret key used for token signing and verification.
        algorithm (str): JWT algorithm used for token signing. Defaults to HS256.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """Initialize the JWT manager.

        Args:
            secret_key: Secret key used for token signing and verification.
                Must be kept secure and should have sufficient entropy.
            algorithm: JWT algorithm to use. Defaults to HS256 (HMAC with SHA-256).
                Should be one of the algorithms supported by PyJWT.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a new JWT access token.

        Creates a token containing the provided data with an expiration time.
        The token is signed using the configured secret key and algorithm.

        Args:
            data: Dictionary of claims to include in the token.
                Should contain user_id and email at minimum.
            expires_delta: Optional custom expiration time.
                If not provided, defaults to 15 minutes.

        Returns:
            JWT token string containing the encoded data and expiration time.

        Example:
            >>> token = jwt_manager.create_access_token(
            ...     data={"user_id": "123", "email": "user@example.com"},
            ...     expires_delta=timedelta(hours=1)
            ... )
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> TokenData:
        """Decode and validate a JWT token.

        Verifies the token signature and expiration time, then extracts the user
        data into a TokenData object.

        Args:
            token: JWT token string to decode and validate.

        Returns:
            TokenData object containing the extracted user information.

        Raises:
            ExpiredTokenError: If the token has expired.
            InvalidTokenError: If the token is malformed or has an invalid signature.

        Example:
            >>> try:
            ...     token_data = jwt_manager.decode_token(token)
            ...     print(f"Token for user: {token_data.email}")
            ... except ExpiredTokenError:
            ...     print("Token has expired")
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenData(
                user_id=UUID(payload["user_id"]),
                email=payload["email"],
                expires_at=datetime.fromtimestamp(payload["exp"]),
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(str(e))
