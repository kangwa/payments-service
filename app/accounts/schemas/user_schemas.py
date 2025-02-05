"""User-related schemas for the accounts domain.

This module provides Pydantic models for handling user-related requests
and responses, including registration, profile updates, and user listings.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.accounts.entities.user import UserStatus
from app.common.value_objects.email import Email


class UserCreateRequest(BaseModel):
    """Schema for user registration requests.

    Args:
        email: Valid email address for the new account.
        password: Strong password meeting security requirements.
        organization_id: UUID of the organization the user belongs to.

    Example:
        >>> request = UserCreateRequest(
        ...     email="new.user@example.com",
        ...     password="SecurePass123!",
        ...     organization_id="123e4567-e89b-12d3-a456-426614174000"
        ... )
    """

    email: EmailStr = Field(
        ...,
        description="Valid email address",
        json_schema_extra={"example": "user@example.com"},
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User password meeting security requirements",
        json_schema_extra={"example": "SecurePass123!"},
    )
    organization_id: UUID = Field(
        ...,
        description="UUID of parent organization",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "organization_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    }


class UserLoginRequest(BaseModel):
    """Schema for user login requests.

    Args:
        email: Registered email address.
        password: Account password.

    Example:
        >>> request = UserLoginRequest(
        ...     email="user@example.com",
        ...     password="SecurePass123!"
        ... )
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address",
        json_schema_extra={"example": "user@example.com"},
    )
    password: str = Field(
        ...,
        description="Account password",
        json_schema_extra={"example": "SecurePass123!"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {"email": "user@example.com", "password": "SecurePass123!"}
        }
    }


class UserResponse(BaseModel):
    """Schema for user data in API responses.

    Args:
        id: Unique user identifier.
        email: User's email address.
        status: Current account status.
        organization_id: UUID of user's organization.
        created_at: Account creation timestamp.
        last_login: Most recent login timestamp.

    Example:
        >>> response = UserResponse(
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     email="user@example.com",
        ...     status=UserStatus.ACTIVE,
        ...     organization_id="987fcdeb-51d2-4ba9-8f3a-123412341234",
        ...     created_at="2024-01-01T00:00:00Z",
        ...     last_login="2024-01-02T15:30:00Z"
        ... )
    """

    id: UUID = Field(
        ...,
        description="Unique user identifier",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    email: Email = Field(
        ...,
        description="User's email address",
        json_schema_extra={"example": "user@example.com"},
    )
    status: UserStatus = Field(
        ...,
        description="Current account status",
        json_schema_extra={"example": UserStatus.ACTIVE},
    )
    organization_id: UUID = Field(
        ...,
        description="User's organization ID",
        json_schema_extra={"example": "987fcdeb-51d2-4ba9-8f3a-123412341234"},
    )
    created_at: datetime = Field(
        ...,
        description="Account creation timestamp",
        json_schema_extra={"example": "2024-01-01T00:00:00Z"},
    )
    last_login: Optional[datetime] = Field(
        None,
        description="Most recent login timestamp",
        json_schema_extra={"example": "2024-01-02T15:30:00Z"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "status": "active",
                "organization_id": "987fcdeb-51d2-4ba9-8f3a-123412341234",
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-02T15:30:00Z",
            }
        },
    )


class UserListResponse(BaseModel):
    """Schema for paginated user list responses.

    Args:
        data: List of user objects.
        total: Total count of users.
        limit: Page size limit.
        offset: Page offset.

    Example:
        >>> response = UserListResponse(
        ...     data=[UserResponse(...)],
        ...     total=100,
        ...     limit=10,
        ...     offset=0
        ... )
    """

    data: List[UserResponse] = Field(..., description="List of user objects")
    total: int = Field(
        ...,
        description="Total number of users",
        json_schema_extra={"example": 100},
        ge=0,
    )
    limit: int = Field(
        ...,
        description="Maximum items per page",
        json_schema_extra={
            "example": 10,
        },
        ge=1,
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
                        "email": "user@example.com",
                        "status": "active",
                        "organization_id": "987fcdeb-51d2-4ba9-8f3a-123412341234",
                        "created_at": "2024-01-01T00:00:00Z",
                        "last_login": "2024-01-02T15:30:00Z",
                    }
                ],
                "total": 100,
                "limit": 10,
                "offset": 0,
            }
        }
    }
