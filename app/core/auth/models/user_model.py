from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from app.core.auth.value_objects import Email, Password


class UserStatus(str, Enum):
    """User account status enumeration.

    Attributes:
        ACTIVE: User account is active and can access the system
        INACTIVE: User account is deactivated but can be reactivated
        SUSPENDED: User account is suspended due to violations
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    """User model representing an authenticated user in the system.

    This model uses custom Email and Password value objects to ensure strong
    validation and normalization of credentials.

    Attributes:
        user_id (UUID): Unique identifier for the user
        email (Email): User's email address, stored as a validated value object
        hashed_password (Password): Securely stored password value object
        status (UserStatus): Current account status
        created_at (datetime): Timestamp of account creation
        last_login (Optional[datetime]): Timestamp of last successful login

    Examples:
        >>> user = User(
        ...     email="John.Doe@EXAMPLE.COM",
        ...     hashed_password="SecurePass123!"
        ... )
        >>> user.email.value
        'John.Doe@example.com'
        >>> str(user.hashed_password)
        '********'
    """

    user_id: UUID = Field(default_factory=uuid4)
    email: Email
    password: Password = None
    hashed_password: str
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

    def activate(self) -> None:
        """Activate the user account.

        Sets the user's status to ACTIVE.
        """
        self.status = UserStatus.ACTIVE

    def deactivate(self) -> None:
        """Deactivate the user account.

        Sets the user's status to INACTIVE.
        """
        self.status = UserStatus.INACTIVE

    def suspend(self) -> None:
        """Suspend the user account.

        Sets the user's status to SUSPENDED.
        """
        self.status = UserStatus.SUSPENDED

    def record_login(self) -> None:
        """Record a successful login attempt.

        Updates the last_login timestamp to the current UTC time.
        """
        self.last_login = datetime.now()

    @property
    def is_active(self) -> bool:
        """Check if the user account is active.

        Returns:
            bool: True if the user's status is ACTIVE, False otherwise
        """
        return self.status == UserStatus.ACTIVE

    class Config:
        """Pydantic model configuration.

        This configuration ensures proper JSON serialization of Email and Password
        value objects by using their string representations.
        """

        json_encoders = {Email: lambda e: e.value, Password: lambda p: str(p)}
