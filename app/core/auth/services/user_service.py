from datetime import timedelta
from app.core.auth.services.commands.auth_commands import CreateUserCommand
from app.core.auth.interfaces import PasswordHasher, UserRepository
from app.core.auth.models import User, UserStatus
from app.core.auth.exceptions import AuthenticationError, TokenError
from app.core.auth.value_objects import Email, Password


class UserService:
    """User service handling user operations.

    This service provides core user functionality including user creation.

    Attributes:
        user_repo (UserRepository): Repository for user persistence operations.
        password_hasher (PasswordHasher): Service for hashing and verifying passwords.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
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

        password = Password(value=command.password)
        hashed_password = self.password_hasher.hash(password.value)
        email = Email(value=command.email)

        user = User(
            email=email,
            hashed_password=hashed_password,
            status=command.status,
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
