from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.core.accounts.dependencies import get_merchant_service
from app.core.accounts.models.user_model import User
from app.core.accounts.schemas.merchant import MerchantCreateRequest, MerchantResponse
from app.core.accounts.services.merchant_service import MerchantService
from app.core.auth.dependencies import get_current_user


router = APIRouter(prefix="/organizations/{org_id}/merchants", tags=["Merchants"])


@router.post("/", response_model=MerchantResponse)
async def create_merchant(
    org_id: UUID,
    data: MerchantCreateRequest,
    service: MerchantService = Depends(get_merchant_service),
    current_user: User = Depends(get_current_user),
):
    """Create a new merchant within an organization.

    Creates a merchant entity associated with the specified organization ID.
    The merchant will be initialized with the provided name, country code,
    and currency settings.

    Args:
        org_id: UUID of the organization to create the merchant under.
        data: Merchant creation data including name, country code, and currency.
        service: Injectable merchant service instance.

    Returns:
        MerchantResponse containing the created merchant's details.

    Raises:
        HTTPException(400): If merchant creation fails due to invalid data
            or business rule violations.

    Example:
        ```
        POST /organizations/123e4567-e89b-12d3-a456-426614174000/merchants/
        {
            "name": "Acme Store",
            "country_code": "US",
            "currency": "USD"
        }
        ```
    """
    try:
        return await service.create_merchant(
            org_id=org_id,
            name=data.name,
            country_code=data.country_code,
            currency=data.currency,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
