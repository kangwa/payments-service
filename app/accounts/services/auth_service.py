"""Authentication service for the accounts domain.

This service handles user authentication, token management, and session control.
It provides a secure interface between the application layer and authentication
infrastructure.
"""

from datetime import timedelta
from typing import Any, Dict
from uuid import UUID

from app.accounts.entities.user import User, UserStatus
from app.accounts.exceptions import (
    AuthenticationError,
    InactiveUserError,
    TokenError,
    UserNotFoundError,
)
from app.accounts.interfaces.user_repo import UserRepository
from app.common.interfaces.password_hasher import PasswordHasher
from app.common.interfaces.token_manager import TokenManager
from app.common.value_objects.email import Email


class AuthService:
    """Authentication service handling user operations and token management.

    This service provides core authentication functionality including:
    - User authentication
    - Token generation and validation
    - Session management
    - Login tracking

    Args:
        user_repo: Repository for user persistence operations.
        password_hasher: Service for secure password operations.
        token_manager: Service for JWT token operations.
        access_token_expire_minutes: Token validity duration in minutes.

    Example:
        >>> auth_service = AuthService(
        ...     user_repo=user_repo,
        ...     password_hasher=password_hasher,
        ...     token_manager=token_manager,
        ...     access_token_expire_minutes=30
        ... )
        >>> user = auth_service.authenticate_user("user@example.com", "password123")
        >>> token = auth_service.create_access_token(user)
    """

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
        access_token_expire_minutes: int = 30,
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_manager = token_manager
        self.access_token_expire = access_token_expire_minutes

    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user with email and password.

        Args:
            email: User's email address.
            password: User's plaintext password.

        Returns:
            Authenticated user entity.

        Raises:
            UserNotFoundError: If user does not exist.
            AuthenticationError: If password is invalid.
            InactiveUserError: If user account is not active.
        """
        user = self.user_repo.get_by_email(email)

        if not user:
            raise UserNotFoundError(
                f"User with email {email} not found", identifier=email
            )

        if not self.password_hasher.verify(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        if user.status != UserStatus.ACTIVE:
            raise InactiveUserError("User account is not active")

        return user

    async def get_logged_in_user(self, token: str) -> User:
        """Get the current user from a JWT token.

        Args:
            token: JWT token string.

        Returns:
            Authenticated user entity.

        Raises:
            TokenError: If token is invalid or expired.
            UserNotFoundError: If user no longer exists.
            InactiveUserError: If user account is not active.
        """
        try:
            payload = self.token_manager.decode_token(token)
            email = Email(payload.get("email"))
            user_id = UUID(payload.get("user_id"))
        except (ValueError, KeyError) as e:
            raise TokenError(f"Invalid token payload: {str(e)}")

        user = self.user_repo.get_by_email(str(email))

        if not user:
            raise UserNotFoundError("User not found")

        if user.id != user_id:
            raise TokenError("Token user ID mismatch")

        if user.status != UserStatus.ACTIVE:
            raise InactiveUserError("User account is not active")

        self.user_repo.update_login_time(user.id)
        return user

    def create_access_token(self, user: User) -> str:
        """Create a JWT access token for a user.

        Args:
            user: User entity to create token for.

        Returns:
            JWT token string.

        Raises:
            ValueError: If user entity is invalid.
        """
        if not user.id or not user.email:
            raise ValueError("Invalid user entity")

        token_data: Dict[str, Any] = {
            "user_id": str(user.id),
            "email": str(user.email),
            "status": user.status.value,
        }

        return self.token_manager.create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=self.access_token_expire),
        )
