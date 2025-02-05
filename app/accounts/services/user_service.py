from uuid import UUID

from app.accounts.entities.user import User, UserStatus
from app.accounts.interfaces.user_repo import UserRepository
from app.accounts.value_objects.password import Password
from app.common.exceptions import ValidationError
from app.common.interfaces.password_hasher import PasswordHasher
from app.common.value_objects.email import Email


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

    def get_user(self, user_id: UUID) -> User:
        """Retrieve a single user by ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            User entity if found

        Raises:
            ValueError: If user is not found
        """
        user = self.repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    def create_user(
        self,
        email_address: str,
        plain_password: str,
        organization_id: UUID,
        status: UserStatus = UserStatus.ACTIVE,
    ) -> User:
        """Create a new user in the system.

        Args:
            command: Command object containing user creation details.

        Returns:
            The newly created user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        email = Email(email_address)
        password = Password(plain_password)

        existing_user = self.user_repo.find_one(
            email.value, {"organization_id": organization_id, "email": email}
        )

        if existing_user:
            raise ValidationError("User already exists")

        hashed_password = self.password_hasher.hash(password.value)
        user = User(
            email=email,
            hashed_password=hashed_password,
            status=status,
            organization_id=organization_id,
        )
        self.user_repo.save(user)
        return user

    def list_users(
        self, org_id: UUID, limit: int, offset: int, status: str = None
    ) -> tuple[list[User], int]:
        """List users using the query handler."""

        query_filter = {"organization_id": org_id}
        if status:
            if status not in UserStatus.__members__:
                raise ValidationError("Invalid status filter")
            query_filter["status"] = UserStatus[status]

        users = self.user_repo.list_all(
            limit=limit, offset=offset, filters=query_filter
        )
        total = self.user_repo.count()

        return users, total
