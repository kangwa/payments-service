from datetime import timedelta
from typing import Optional

from app.core.auth.interfaces import PasswordHasher, TokenManager, UserRepository
from app.core.auth.models import User


class AuthService:
    """Authentication service handling user operations and token management.

    This service provides core authentication functionality including user creation,
    authentication, token generation and validation. It encapsulates all authentication-related
    business logic and coordinates between the user repository, password hasher, and token manager.

    Attributes:
        user_repo (UserRepository): Repository for user persistence operations.
        password_hasher (PasswordHasher): Service for hashing and verifying passwords.
        token_manager (TokenManager): Service for JWT token operations.
        access_token_expire (int): Token expiration time in minutes.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
        access_token_expire_minutes: int = 30,
    ):
        """Initialize the authentication service.

        Args:
            user_repo: Repository for user persistence operations.
            password_hasher: Service for hashing and verifying passwords.
            token_manager: Service for JWT token operations.
            access_token_expire_minutes: Token expiration time in minutes. Defaults to 30.
        """
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_manager = token_manager
        self.access_token_expire = access_token_expire_minutes

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password.

        Args:
            email: The user's email address.
            password: The user's plain text password.

        Returns:
            User if authentication succeeds, None otherwise.

        Note:
            This method does not raise exceptions for authentication failures,
            instead returning None to allow the caller to handle the failure case.
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not self.password_hasher.verify(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, user: User) -> str:
        """Create a JWT access token for a user.

        Args:
            user: The user for whom to create the token.

        Returns:
            A JWT token string containing user identification data.

        Note:
            Token includes user_id and email claims and expires based on
            the configured access_token_expire time.
        """
        return self.token_manager.create_access_token(
            data={"user_id": str(user.user_id), "email": user.email},
            expires_delta=timedelta(minutes=self.access_token_expire),
        )
