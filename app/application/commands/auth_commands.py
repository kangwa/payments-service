from dataclasses import dataclass
from uuid import UUID
from app.domain.models.auth import UserStatus


@dataclass
class CreateUserCommand:
    """Command for creating a new user in the system.

    This class represents a command to create a user with basic authentication details.
    It follows the Command pattern and is immutable by design using the @dataclass decorator.

    Attributes:
        email (str): The user's email address that will serve as their unique identifier.
            Must be a valid email format.
        password (str): The user's password in plain text. This should be hashed before storage.
        status (UserStatus, optional): The initial status of the user account.
            Defaults to UserStatus.ACTIVE.

    Example:
        >>> command = CreateUserCommand(
        ...     email="user@example.com",
        ...     password="secure_password123",
        ...     status=UserStatus.ACTIVE
        ... )
    """

    email: str
    password: str
    status: UserStatus = UserStatus.ACTIVE
    initiated_by: UUID = None
