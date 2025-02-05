"""Merchant-related schemas for the accounts domain.

This module provides Pydantic models for handling merchant-related requests
and responses, including creation, updates, and merchant listings.
"""

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.accounts.entities.merchant import MerchantStatus


class MerchantCreateRequest(BaseModel):
    """Schema for merchant creation requests.

    Args:
        name: Legal business name of the merchant.
        country_code: ISO 3166-1 alpha-2 country code.
        currency: ISO 4217 currency code.
        status: Initial merchant status.
        organization_id: Parent organization identifier.

    Example:
        >>> request = MerchantCreateRequest(
        ...     name="Acme Store",
        ...     country_code="US",
        ...     currency="USD",
        ...     status=MerchantStatus.ACTIVE,
        ...     organization_id="123e4567-e89b-12d3-a456-426614174000"
        ... )
    """

    name: str = Field(
        ...,
        description="Legal business name",
        json_schema_extra={"example": "Acme Store"},
        min_length=1,
        max_length=100,
    )
    country_code: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code",
        json_schema_extra={"example": "US"},
        pattern="^[A-Z]{2}$",
        min_length=2,
        max_length=2,
    )
    currency: str = Field(
        ...,
        description="ISO 4217 currency code",
        json_schema_extra={"example": "USD"},
        pattern="^[A-Z]{3}$",
        min_length=3,
        max_length=3,
    )
    status: MerchantStatus = Field(
        default=MerchantStatus.ACTIVE, description="Initial merchant status"
    )
    organization_id: UUID = Field(
        ...,
        description="Parent organization ID",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Acme Store",
                "country_code": "US",
                "currency": "USD",
                "status": "active",
                "organization_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    }


class MerchantResponse(BaseModel):
    """Schema for merchant data in API responses.

    Args:
        id: Unique merchant identifier.
        name: Legal business name.
        country_code: ISO country code.
        currency: ISO currency code.
        status: Current merchant status.

    Example:
        >>> response = MerchantResponse(
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     name="Acme Store",
        ...     country_code="US",
        ...     currency="USD",
        ...     status="active"
        ... )
    """

    id: UUID = Field(
        ...,
        description="Unique merchant identifier",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    name: str = Field(
        ...,
        description="Legal business name",
        json_schema_extra={"example": "Acme Store"},
    )
    country_code: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code",
        json_schema_extra={"example": "US"},
    )
    currency: str = Field(
        ..., description="ISO 4217 currency code", json_schema_extra={"example": "USD"}
    )
    status: str = Field(
        ...,
        description="Current merchant status",
        json_schema_extra={"example": "active"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Acme Store",
                "country_code": "US",
                "currency": "USD",
                "status": "active",
            }
        },
    )


class MerchantListResponse(BaseModel):
    """Schema for paginated merchant list responses.

    Args:
        data: List of merchant objects.
        total: Total count of merchants.
        limit: Page size limit.
        offset: Page offset.

    Example:
        >>> response = MerchantListResponse(
        ...     data=[MerchantResponse(...)],
        ...     total=100,
        ...     limit=10,
        ...     offset=0
        ... )
    """

    data: List[MerchantResponse] = Field(..., description="List of merchant objects")
    total: int = Field(
        ...,
        description="Total number of merchants",
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
                        "name": "Acme Store",
                        "country_code": "US",
                        "currency": "USD",
                        "status": "active",
                    }
                ],
                "total": 100,
                "limit": 10,
                "offset": 0,
            }
        }
    }
