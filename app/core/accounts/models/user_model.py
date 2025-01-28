from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


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

    Attributes:
        user_id (UUID): Unique identifier for the user
        email (EmailStr): User's email address
        hashed_password (str): Securely hashed password
        status (UserStatus): Current account status
        created_at (datetime): Timestamp of account creation
        last_login (Optional[datetime]): Timestamp of last successful login
    """

    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr
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
