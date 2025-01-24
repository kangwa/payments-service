from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class CreateOrganization:
    """Command for creating a new organization.

    This command encapsulates the data required to create an organization,
    automatically generating a UUID if none is provided.

    Attributes:
        name: Name of the organization to create.
        id: Optional UUID for the organization. If not provided, one will be
            generated during initialization.

    Example:
        >>> cmd = CreateOrganization("Acme Corp")
        >>> print(cmd.id)  # Auto-generated UUID
    """

    name: str
    initiated_by: UUID = None
    id: UUID = None

    def __post_init__(self):
        """Initialize organization ID if not provided.

        Automatically generates a UUID v4 for the organization if one was
        not specified during instantiation.
        """
        if self.id is None:
            self.id = uuid4()


@dataclass
class SuspendOrganization:
    """Command for suspending an existing organization.

    This command represents the intent to suspend an organization's operations,
    preventing further activity while maintaining historical data.

    Attributes:
        organization_id: UUID of the organization to suspend.

    Example:
        >>> cmd = SuspendOrganization(UUID('123e4567-e89b-12d3-a456-426614174000'))
    """

    organization_id: UUID
    initiated_by: UUID = None
