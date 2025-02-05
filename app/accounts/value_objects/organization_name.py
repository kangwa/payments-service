from typing import ClassVar

from pydantic import BaseModel, ConfigDict, field_validator


class OrganizationName(BaseModel):
    """Value object representing an organization name.

    Validates and normalizes organization names according to business rules.

    Args:
        value: Organization name string to validate and normalize.

    Example:
        >>> name = OrganizationName("  Acme Corporation  ")
        >>> str(name)
        'Acme Corporation'
    """

    value: str

    model_config = ConfigDict(frozen=True)

    MIN_LENGTH: ClassVar[int] = 2
    MAX_LENGTH: ClassVar[int] = 100

    @field_validator("value", mode="before")
    @classmethod
    def validate_and_normalize_name(cls, v: str) -> str:
        """Validate and normalize organization name.

        Args:
            v: Organization name to validate.

        Returns:
            Normalized organization name.

        Raises:
            ValueError: If name is invalid.
        """
        if not v:
            raise ValueError("Organization name cannot be empty")

        name = v.strip()

        if len(name) < cls.MIN_LENGTH:
            raise ValueError(
                f"Organization name must be at least {cls.MIN_LENGTH} characters"
            )

        if len(name) > cls.MAX_LENGTH:
            raise ValueError(
                f"Organization name must be less than {cls.MAX_LENGTH} characters"
            )

        # Prevent names with only whitespace/special characters
        if not any(c.isalnum() for c in name):
            raise ValueError(
                "Organization name must contain at least one alphanumeric character"
            )

        return name

    def __str__(self) -> str:
        """String representation of organization name.

        Returns:
            Normalized organization name string.
        """
        return self.value
