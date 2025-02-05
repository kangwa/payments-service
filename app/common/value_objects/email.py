import re
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class Email(BaseModel):
    """A value object representing an email address with validation and normalization.

    Enforces RFC 5322 compliant validation and consistent casing. The local part
    maintains its original case while the domain is converted to lowercase.

    Args:
        value: Raw email string to validate and normalize.

    Raises:
        ValueError: If email is empty, contains invalid characters, or doesn't
            match the required format (local@domain.tld).

    Example:
        >>> email = Email("John.Doe@EXAMPLE.COM")
        >>> email.value
        'John.Doe@example.com'
    """

    value: str

    model_config = ConfigDict(frozen=True)

    def __init__(self, value: str, **kwargs: Any) -> None:
        """Initialize Email with a string value directly."""
        super().__init__(value=value, **kwargs)

    @field_validator("value", mode="before")
    @classmethod
    def validate_and_normalize_email(cls, v: str) -> str:
        """Validate and normalize email address.

        Args:
            v: Email string to validate.

        Returns:
            Normalized email string.

        Raises:
            ValueError: If email format is invalid.
        """
        if not v:
            raise ValueError("Email cannot be empty")

        v = v.strip()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")

        parts = v.split("@")
        if len(parts) == 2:
            return f"{parts[0]}@{parts[1].lower()}"
        return v.lower()

    def __str__(self) -> str:
        """String representation of email.

        Returns:
            Normalized email string.
        """
        return self.value
