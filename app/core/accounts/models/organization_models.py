from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum


class OrganizationStatus(str, Enum):
    """Organization status enumeration.

    Attributes:
        ACTIVE: Organization is active and operational
        SUSPENDED: Organization access has been suspended
        PENDING: Organization is pending approval/activation
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"


class Organization(BaseModel):
    """Organization model representing a business entity.

    Attributes:
        id (UUID): Unique identifier for the organization
        name (str): Organization name
        created_at (datetime): Timestamp of organization creation
        updated_at (datetime): Timestamp of last update
        status (OrganizationStatus): Current organization status
        metadata (dict): Additional organization metadata
    """

    id: UUID = uuid4()
    name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: OrganizationStatus = OrganizationStatus.PENDING
    metadata: dict = {}

    def activate(self) -> None:
        """Activate the organization.

        Sets status to ACTIVE and updates the updated_at timestamp.
        """
        self.status = OrganizationStatus.ACTIVE
        self.updated_at = datetime.now()

    def suspend(self) -> None:
        """Suspend the organization.

        Sets status to SUSPENDED and updates the updated_at timestamp.
        """
        self.status = OrganizationStatus.SUSPENDED
        self.updated_at = datetime.now()
