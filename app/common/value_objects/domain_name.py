import re
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, field_validator


class DomainName(BaseModel):
    """Value object representing a valid domain name.

    Validates and normalizes domain names according to RFC 1035 standards.

    Args:
        value: Domain name string to validate and normalize.

    Example:
        >>> domain = DomainName("EXAMPLE.COM")
        >>> str(domain)
        'example.com'
    """

    value: str

    model_config = ConfigDict(frozen=True)

    # Class constants with type annotations
    DOMAIN_PATTERN: ClassVar[str] = r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
    MAX_LENGTH: ClassVar[int] = 253  # RFC 1035 limit

    @field_validator("value", mode="before")
    @classmethod
    def validate_and_normalize_domain(cls, v: str) -> str:
        """Validate and normalize domain name.

        Args:
            v: Domain name to validate.

        Returns:
            Normalized lowercase domain name.

        Raises:
            ValueError: If domain format is invalid.
        """
        if not v:
            raise ValueError("Domain name cannot be empty")

        domain = v.strip().lower()

        if len(domain) > cls.MAX_LENGTH:
            raise ValueError(f"Domain must be less than {cls.MAX_LENGTH} characters")

        if not re.match(cls.DOMAIN_PATTERN, domain):
            raise ValueError(
                "Invalid domain format. Must be a valid domain name (e.g., example.com)"
            )

        return domain

    def __str__(self) -> str:
        """String representation of domain name.

        Returns:
            Normalized domain name string.
        """
        return self.value

    def __eq__(self, other: Any) -> bool:
        """Compare domain names case-insensitively."""
        if not isinstance(other, DomainName):
            return False
        return self.value.lower() == other.value.lower()
