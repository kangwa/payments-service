from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class OrganizationStatus(str, Enum):
    """Organization operational status enumeration.

    Args:
        ACTIVE: Organization is operational with full system access.
        SUSPENDED: Organization access has been temporarily revoked.
        PENDING: Organization awaiting activation approval.
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"


class Organization(BaseModel):
    """Organization aggregate root representing a business entity.

    This entity manages the lifecycle and state of organizations in the system.
    Organizations serve as the top-level container for users and merchants.

    Args:
        id: Unique identifier for the organization.
        name: Official organization name.
        domain: Primary email domain for the organization.
        created_at: Timestamp of organization creation.
        updated_at: Timestamp of last modification.
        status: Current operational status.
        metadata: Additional organization context data.

    Example:
        >>> org = Organization(
        ...     name="Acme Corp",
        ...     domain="acme.com"
        ... )
        >>> org.activate()
        >>> org.status
        <OrganizationStatus.ACTIVE>
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    domain: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: OrganizationStatus = OrganizationStatus.PENDING
    metadata: Dict = Field(default_factory=dict)

    @field_validator("domain")
    def validate_domain(cls, v: str) -> str:
        """Validate organization domain format.

        Args:
            v: Domain name to validate.

        Returns:
            Normalized lowercase domain name.

        Raises:
            ValueError: If domain format is invalid.
        """
        if not v or "." not in v:
            raise ValueError("Invalid domain format")
        return v.lower()

    def activate(self) -> None:
        """Activate the organization.

        Transitions status to ACTIVE and updates modification timestamp.
        Only active organizations can access system services.
        """
        self.status = OrganizationStatus.ACTIVE
        self.updated_at = datetime.now()

    def suspend(self) -> None:
        """Suspend the organization.

        Transitions status to SUSPENDED and updates modification timestamp.
        Suspended organizations cannot access any system services.
        """
        self.status = OrganizationStatus.SUSPENDED
        self.updated_at = datetime.now()

    @property
    def is_active(self) -> bool:
        """Check if organization is active.

        Returns:
            True if status is ACTIVE, False otherwise.
        """
        return self.status == OrganizationStatus.ACTIVE
