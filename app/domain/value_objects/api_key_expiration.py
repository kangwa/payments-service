from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class ApiKeyExpiration(BaseModel):
    """Value object representing API key expiration.

    Uses None to represent never-expiring keys instead of string values.

    Attributes:
        value: datetime for expiring keys, None for never-expiring keys
    """

    value: Optional[datetime] = None

    @field_validator("value")
    def validate_value(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate the expiration value.

        Args:
            v: The expiration datetime or None

        Returns:
            The validated datetime or None

        Raises:
            ValueError: If datetime is not in the future
        """
        if v is not None and v <= datetime.now():
            raise ValueError("Expiration must be in the future")
        return v

    @classmethod
    def create(cls, expiration: Optional[datetime]) -> "ApiKeyExpiration":
        """Create an ApiKeyExpiration instance.

        Args:
            expiration: Optional expiration datetime. None means never expires.

        Returns:
            ApiKeyExpiration instance
        """
        return cls(value=expiration)

    @classmethod
    def never_expires(cls) -> "ApiKeyExpiration":
        """Create a never-expiring instance.

        Returns:
            ApiKeyExpiration instance that never expires
        """
        return cls(value=None)

    def is_expired(self) -> bool:
        """Check if the expiration has passed.

        Returns:
            bool: True if there is an expiration datetime and it has passed
        """
        return self.value is not None and self.value < datetime.now()

    def to_datetime(self) -> Optional[datetime]:
        """Get the expiration datetime.

        Returns:
            datetime if an expiration is set, None if never expires
        """
        return self.value
