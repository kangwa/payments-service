from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from app.accounts.value_objects.password import Password
from app.common.value_objects.email import Email


class UserStatus(str, Enum):
    """User account status enumeration.

    Args:
        ACTIVE: User has full system access.
        INACTIVE: User account is deactivated.
        SUSPENDED: User access has been revoked.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    """User aggregate root representing an authenticated system user.

    This entity manages user authentication state and profile data.
    It uses Email and Password value objects for secure credential handling.

    Args:
        id: Unique identifier for the user.
        email: User's email address as Email value object.
        organization_id: Reference to parent organization.
        hashed_password: Securely hashed password string.
        name: User's full name.
        password: Optional raw password for creation/updates.
        status: Current account status.
        created_at: Timestamp of account creation.
        last_login: Timestamp of most recent login.

    Example:
        >>> user = User(
        ...     email=Email("john.doe@example.com"),
        ...     organization_id=uuid4(),
        ...     name="John Doe",
        ...     hashed_password="hashed_secret"
        ... )
        >>> user.email.value
        'john.doe@example.com'
    """

    id: UUID = Field(default_factory=uuid4)
    email: Email
    organization_id: UUID
    hashed_password: str
    name: Optional[str] = None
    password: Optional[Password] = None
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('email')
    def serialize_email(self, email: Email, _info):
        return str(email)
    
    @field_serializer('password')
    def serialize_email(self, password: Password, _info):
        return str(password)

    @field_validator("name")
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate user name format.

        Args:
            v: Name to validate.

        Returns:
            Normalized name string or None.

        Raises:
            ValueError: If name is empty string.
        """
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty string")
        return v.strip() if v else None

    def activate(self) -> None:
        """Activate the user account.

        Transitions status to ACTIVE allowing system access.
        """
        self.status = UserStatus.ACTIVE

    def deactivate(self) -> None:
        """Deactivate the user account.

        Transitions status to INACTIVE preventing system access.
        """
        self.status = UserStatus.INACTIVE

    def suspend(self) -> None:
        """Suspend the user account.

        Transitions status to SUSPENDED due to possible violations.
        """
        self.status = UserStatus.SUSPENDED

    def record_login(self) -> None:
        """Record a successful login attempt.

        Updates the last_login timestamp to current time.
        """
        self.last_login = datetime.now()

    @property
    def is_active(self) -> bool:
        """Check if user account is active.

        Returns:
            True if status is ACTIVE, False otherwise.
        """
        return self.status == UserStatus.ACTIVE
