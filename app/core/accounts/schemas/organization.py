from typing import List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class OrganizationCreateRequest(BaseModel):
    """Schema for organization creation requests.

    Attributes:
        name: Name of the organization. Will be used as the display name
            and for identification purposes.
    """

    name: str


class OrganizationResponse(BaseModel):
    """Schema for organization data in API responses.

    Handles serialization of organization entities for API responses.

    Attributes:
        id: Unique identifier for the organization.
        name: Organization's display name.
        status: Current organization status (e.g., 'ACTIVE', 'SUSPENDED').
        created_at: Timestamp when the organization was created.
    """

    id: UUID
    name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    """Schema for paginated organization list responses.

    Contains both the list of organizations and pagination metadata.

    Attributes:
        data: List of organization objects matching query criteria.
        total: Total count of organizations matching query (before pagination).
        limit: Maximum number of items per page.
        offset: Number of items skipped for pagination.

    Example:
        ```json
        {
            "data": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Acme Corp",
                    "status": "ACTIVE",
                    "created_at": "2024-01-23T10:20:30.123Z"
                }
            ],
            "total": 50,
            "limit": 10,
            "offset": 0
        }
        ```
    """

    data: List[OrganizationResponse]
    total: int
    limit: int
    offset: int
