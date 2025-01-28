from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID

from app.core.auth.models.user_model import User
from app.core.auth.value_objects import Email


class TokenData(BaseModel):
    """Authentication token data model.

    This model uses the Email value object to ensure consistent
    validation and normalization of email addresses in tokens.

    Attributes:
        user_id (UUID): ID of the user the token belongs to
        email (Email): Email address associated with the token, stored as a validated value object
        expires_at (datetime): Token expiration timestamp

    Examples:
        >>> user = User(user_id=UUID('...'), email=Email('user@EXAMPLE.com'))
        >>> token = TokenData.create_token(user, timedelta(hours=1))
        >>> token.email.value
        'user@example.com'
    """

    user_id: UUID
    email: Email
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired.

        Returns:
            bool: True if current time is past expires_at, False otherwise
        """
        return datetime.now() > self.expires_at

    @classmethod
    def create_token(cls, user: User, expires_in: timedelta) -> "TokenData":
        """Create a new token for a user.

        Args:
            user (User): User to create token for. Must have valid user_id and email.
            expires_in (timedelta): Token validity duration

        Returns:
            TokenData: New token data instance with normalized email
        """
        return cls(
            user_id=user.user_id,
            email=user.email,  # Email is already a value object from User model
            expires_at=datetime.now() + expires_in,
        )

    class Config:
        """Pydantic model configuration.

        Ensures proper JSON serialization of Email value object by using
        its string representation.
        """

        json_encoders = {Email: lambda e: e.value}
