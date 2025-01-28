from pydantic import BaseModel
from uuid import UUID


class MerchantCreateRequest(BaseModel):
    """Schema for merchant creation requests.

    Attributes:
        name: Business name of the merchant.
        country_code: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB').
        currency: Three-letter ISO 4217 currency code (e.g., 'USD', 'EUR').
    """

    name: str
    country_code: str
    currency: str


class MerchantResponse(BaseModel):
    """Schema for merchant data in API responses.

    Handles serialization of merchant entities for API responses.

    Attributes:
        id: Unique identifier for the merchant.
        name: Business name of the merchant.
        country_code: Two-letter ISO country code where merchant operates.
        currency: Three-letter ISO currency code for merchant's primary currency.
        status: Current merchant status (e.g., 'ACTIVE', 'SUSPENDED').

    Note:
        Configured to automatically convert from ORM models using from_attributes.
    """

    id: UUID
    name: str
    country_code: str
    currency: str
    status: str

    class Config:
        from_attributes = True
