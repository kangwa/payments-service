import re
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


class Password(BaseModel):
    """A value object representing a password with strong complexity requirements.

    Enforces password security rules including minimum length and character variety.
    The actual value is never exposed in string representation.

    Args:
        value: Raw password string to validate.

    Raises:
        ValidationError: If password fails any complexity requirements:
            - Minimum length of 8 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character

    Example:
        >>> password = Password("SecurePass123!")
        >>> str(password)
        '********'
    """

    value: str

    model_config = ConfigDict(frozen=True)

    def __init__(self, value: str, **kwargs: Any) -> None:
        """Initialize Password with a string value directly."""
        super().__init__(value=value, **kwargs)

    @field_validator("value")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        """Validate password meets complexity requirements.

        Args:
            v: Password string to validate.

        Returns:
            Validated password string.

        Raises:
            ValidationError: If password doesn't meet requirements.
        """
        errors = []

        if len(v) < 8:
            errors.append(
                {
                    "type": "value_error",
                    "loc": ("password",),
                    "msg": "Must be at least 8 characters long",
                    "input": v,
                    "ctx": {"error": ValueError("Must be at least 8 characters long")},
                }
            )

        if not re.search(r"[A-Z]", v):
            errors.append(
                {
                    "type": "value_error",
                    "loc": ("password",),
                    "msg": "At least one uppercase letter required",
                    "input": v,
                    "ctx": {
                        "error": ValueError("At least one uppercase letter required")
                    },
                }
            )

        if not re.search(r"[a-z]", v):
            errors.append(
                {
                    "type": "value_error",
                    "loc": ("password",),
                    "msg": "At least one lowercase letter required",
                    "input": v,
                    "ctx": {
                        "error": ValueError("At least one lowercase letter required")
                    },
                }
            )

        if not re.search(r"\d", v):
            errors.append(
                {
                    "type": "value_error",
                    "loc": ("password",),
                    "msg": "At least one digit required",
                    "input": v,
                    "ctx": {"error": ValueError("At least one digit required")},
                }
            )

        if not re.search(r"[^A-Za-z0-9]", v):
            errors.append(
                {
                    "type": "value_error",
                    "loc": ("password",),
                    "msg": "At least one special character required",
                    "input": v,
                    "ctx": {
                        "error": ValueError("At least one special character required")
                    },
                }
            )

        if errors:
            raise ValidationError.from_exception_data(
                "Password validation failed", line_errors=errors
            )

        return v

    def __str__(self) -> str:
        """Secure string representation.

        Returns:
            Masked password string.
        """
        return "********"


class HashedPassword(BaseModel):
    """A value object representing a hashed password.

    Used to store password hashes securely, as opposed to the Password class
    which handles raw password validation.

    Args:
        value: Hashed password string.

    Example:
        >>> hashed = HashedPassword("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LedYQNB8UHUHzh/ra")
        >>> str(hashed)
        '********'
    """

    value: str

    model_config = ConfigDict(frozen=True)

    def __init__(self, value: str, **kwargs: Any) -> None:
        """Initialize HashedPassword with a string value directly."""
        super().__init__(value=value, **kwargs)

    def __str__(self) -> str:
        """Secure string representation.

        Returns:
            Masked password string.
        """
        return "********"
