from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ListOrganizations:
    """Command for retrieving a paginated list of organizations.

    This command encapsulates the parameters needed for paginated organization listing,
    with optional status filtering.

    Attributes:
        limit: Maximum number of organizations to return.
        offset: Number of organizations to skip (for pagination).
        status: Optional filter for organization status.
            If provided, only organizations matching this status will be returned.

    Example:
        >>> cmd = ListOrganizations(limit=10, offset=0, status="ACTIVE")
        >>> # Will return up to 10 active organizations, starting from index 0
    """

    limit: int
    offset: int
    initiated_by: UUID = None
    status: Optional[str] = None


@dataclass
class GetOrganization:
    """Command for retrieving a specific organization by ID.

    This command represents a request to fetch detailed information
    about a single organization.

    Attributes:
        organization_id: UUID of the organization to retrieve.

    Example:
        >>> cmd = GetOrganization(UUID('123e4567-e89b-12d3-a456-426614174000'))
    """

    organization_id: UUID
    initiated_by: UUID = None
