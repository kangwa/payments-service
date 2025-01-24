from datetime import timedelta
from typing import Optional
from app.application.commands.auth_commands import CreateUserCommand
from app.domain.interfaces.auth import PasswordHasher, TokenManager
from app.domain.models.auth import User, UserStatus
from app.domain.repositories.auth import UserRepository
from app.exceptions import AuthenticationError, TokenError


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

    async def create_user(self, command: CreateUserCommand) -> User:
        """Create a new user in the system.

        Args:
            command: Command object containing user creation details.

        Returns:
            The newly created user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        existing_user = await self.user_repo.get_by_email(command.email)
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = self.password_hasher.hash(command.password)

        user = User(
            email=command.email, hashed_password=hashed_password, status=command.status
        )

        await self.user_repo.save(user)
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

    async def get_current_user(self, token: str) -> User:
        """Get the current user from a JWT token.

        This method validates the token, retrieves the corresponding user,
        and updates their last login time.

        Args:
            token: JWT token string.

        Returns:
            The authenticated user.

        Raises:
            AuthenticationError: If token is invalid or user validation fails.
            ValueError: If user is not found or inactive.
        """
        try:
            token_data = self.token_manager.decode_token(token)
            user = await self.user_repo.get_by_email(token_data.email)

            if not user:
                raise ValueError("User not found")

            if user.status != UserStatus.ACTIVE:
                raise ValueError("Inactive user")

            await self.user_repo.update_login_time(user.user_id)
            return user

        except TokenError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
