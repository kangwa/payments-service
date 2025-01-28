from pydantic import BaseModel, field_validator, StringConstraints, ConfigDict
from typing import Annotated
import re


class Email(BaseModel):
    """
    A value object representing an email address with validation and normalization.

    This class ensures that email addresses are properly formatted and normalized
    by enforcing RFC 5322 compliant validation and consistent casing.

    Attributes:
        value (str): The normalized and validated email address. The local part
            maintains its original case while the domain is converted to lowercase.

    Raises:
        ValueError: If the email is empty, contains invalid characters, or doesn't
            match the required format (local@domain.tld).

    Examples:
        >>> email = Email(value=" John.Doe@EXAMPLE.COM ")
        >>> email.value
        'John.Doe@example.com'

        >>> invalid_email = Email(value="not-an-email")
        Traceback (most recent call last):
            ...
        ValueError: Invalid email format
    """

    value: str

    model_config = ConfigDict(frozen=True)

    @field_validator("value", mode="before")
    @classmethod
    def validate_and_normalize_email(cls, v: str) -> str:
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
        return self.value


class Password(BaseModel):
    """
    A value object representing a password with strong complexity requirements.

    This class enforces password security rules including minimum length,
    character variety, and safe string representation.

    Attributes:
        value (str): The validated password meeting all complexity requirements.
            The actual value is never exposed in string representation.

    Raises:
        ValueError: If the password fails any of the following requirements:
            - Minimum length of 8 characters
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character
    """

    value: Annotated[str, StringConstraints(min_length=8)]

    model_config = ConfigDict(frozen=True)

    @field_validator("value")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        errors = []

        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", v):
            errors.append("At least one uppercase letter required")

        if not re.search(r"[a-z]", v):
            errors.append("At least one lowercase letter required")

        if not re.search(r"\d", v):
            errors.append("At least one digit required")

        if not re.search(r"[^A-Za-z0-9]", v):
            errors.append("At least one special character required")

        if errors:
            raise ValueError("; ".join(errors))

        return v
    
    def __str__(self) -> str:
        return "********"


class HashedPassword(BaseModel):
    """
    A value object representing a hashed password.
    
    This class is used to store password hashes, as opposed to the Password
    class which handles raw password validation.

    Attributes:
        value (str): The hashed password value.
    """
    value: str

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        return "********"
