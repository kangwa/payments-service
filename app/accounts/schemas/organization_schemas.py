"""Organization-related schemas for the accounts domain.

This module provides Pydantic models for handling organization-related requests
and responses, including creation, updates, and organization listings.
"""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreateRequest(BaseModel):
    """Schema for organization creation requests.

    Args:
        name: Organization's display name.
        domain: Organization's email domain.

    Example:
        >>> request = OrganizationCreateRequest(
        ...     name="Acme Corporation",
        ...     domain="acme.com"
        ... )
    """

    name: str = Field(
        ...,
        description="Organization display name",
        json_schema_extra={"example": "Acme Corporation"},
        min_length=1,
        max_length=100,
    )
    domain: str = Field(
        ...,
        description="Organization email domain",
        json_schema_extra={"example": "acme.com"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {"name": "Acme Corporation", "domain": "acme.com"}
        }
    }


class OrganizationResponse(BaseModel):
    """Schema for organization data in API responses.

    Args:
        id: Unique organization identifier.
        name: Organization display name.
        domain: Current organization domain.
        status: Current organization status.
        created_at: Organization creation timestamp.

    Example:
        >>> response = OrganizationResponse(
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     name="Acme Corporation",
        ...     status="active",
        ...     domain="acme.com",
        ...     created_at="2024-01-01T00:00:00Z"
        ... )
    """

    id: UUID = Field(
        ...,
        description="Unique organization identifier",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    name: str = Field(
        ...,
        description="Organization display name",
        json_schema_extra={"example": "Acme Corporation"},
    )
    domain: str = Field(
        ...,
        description="Organization domain name",
        json_schema_extra={"example": "acme.com"},
    )
    status: str = Field(
        ...,
        description="Current organization status",
        json_schema_extra={"example": "active"},
    )
    created_at: datetime = Field(
        ...,
        description="Organization creation timestamp",
        json_schema_extra={"example": "2024-01-01T00:00:00Z"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Acme Corporation",
                "domain": "acme.com",
                "status": "active",
                "created_at": "2024-01-01T00:00:00Z",
            }
        },
    )


class OrganizationListResponse(BaseModel):
    """Schema for paginated organization list responses.

    Args:
        data: List of organization objects.
        total: Total count of organizations.
        limit: Page size limit.
        offset: Page offset.

    Example:
        >>> response = OrganizationListResponse(
        ...     data=[OrganizationResponse(...)],
        ...     total=100,
        ...     limit=10,
        ...     offset=0
        ... )
    """

    data: List[OrganizationResponse] = Field(
        ..., description="List of organization objects"
    )
    total: int = Field(
        ...,
        description="Total number of organizations",
        json_schema_extra={"example": 100},
        ge=0,
    )
    limit: int = Field(
        ...,
        description="Maximum items per page",
        json_schema_extra={"example": 10},
        ge=1,
        le=1000,
    )
    offset: int = Field(
        ...,
        description="Number of items to skip",
        json_schema_extra={"example": 0},
        ge=0,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Acme Corporation",
                        "status": "active",
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "total": 100,
                "limit": 10,
                "offset": 0,
            }
        }
    }
