"""TokenData entity for managing authentication tokens."""

from datetime import datetime, timedelta
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer

from app.common.value_objects.email import Email


class TokenData(BaseModel):
    """Authentication token data model.

    A domain entity representing an authentication token with built-in
    expiration handling and email validation.

    Args:
        user_id: ID of the associated user.
        email: Email address as Email value object.
        expires_at: Token expiration timestamp.

    Example:
        >>> from uuid import uuid4
        >>> token = TokenData(
        ...     user_id=uuid4(),
        ...     email=Email("user@example.com"),
        ...     expires_at=datetime.now() + timedelta(hours=1)
        ... )
        >>> token.is_expired
        False
    """

    user_id: UUID
    email: Email
    expires_at: datetime

    @field_serializer('email')
    def serialize_email(self, email: Email, _info):
        return str(email)

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired.

        Returns:
            True if current time is past expires_at.
        """
        return datetime.now() > self.expires_at

    @classmethod
    def create_token(
        cls, user_id: UUID, email: Email, expires_in: timedelta
    ) -> "TokenData":
        """Create a new token with specified expiration.

        Args:
            user_id: ID of the user to create token for.
            email: User's email as Email value object.
            expires_in: Token validity duration.

        Returns:
            New token instance.

        Example:
            >>> from datetime import timedelta
            >>> from uuid import uuid4
            >>> token = TokenData.create_token(
            ...     user_id=uuid4(),
            ...     email=Email("user@example.com"),
            ...     expires_in=timedelta(hours=1)
            ... )
        """
        return cls(
            user_id=user_id,
            email=email,
            expires_at=datetime.now() + expires_in,
        )
