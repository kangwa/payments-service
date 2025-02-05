from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.accounts.ports.rest.dependencies import get_merchant_service
from app.accounts.schemas.merchant_schemas import (
    MerchantCreateRequest,
    MerchantListResponse,
    MerchantResponse,
)
from app.accounts.services.merchant_service import MerchantService
from app.common.exceptions import ValidationError

router = APIRouter(prefix="/organizations/{org_id}/merchants", tags=["Merchants"])


@router.get("/", response_model=MerchantListResponse)
def list_merchants(
    org_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: str = Query(None),
    service: MerchantService = Depends(get_merchant_service),
):
    """List organizations with pagination and optional status filtering.

    Retrieves a paginated list of organizations that can be filtered by their
    status (e.g., 'ACTIVE', 'SUSPENDED').

    Args:
        limit: Maximum number of organizations to return (1-1000).
        offset: Number of organizations to skip for pagination.
        status: Optional filter for organization status.
        service: Injectable organization service instance.

    Returns:
        OrganizationListResponse containing:
            - List of organizations matching criteria
            - Total count of matching organizations
            - Applied limit and offset values

    Raises:
        HTTPException(400): If status filter value is invalid.

    Example:
        ```
        GET /organizations/?limit=50&offset=0&status=ACTIVE
        ```
    """
    try:
        merchants, total = service.list_merchants(
            limit=limit, offset=offset, status=status, org_id=org_id
        )

        return {"data": merchants, "total": total, "limit": limit, "offset": offset}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.post("/", response_model=MerchantResponse, status_code=status.HTTP_201_CREATED)
def create_merchant(
    org_id: UUID,
    data: MerchantCreateRequest,
    service: MerchantService = Depends(get_merchant_service),
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
        merchant = service.create_merchant(
            org_id=org_id,
            name=data.name,
            country_code=data.country_code,
            currency=data.currency,
        )
        return merchant
    except ValidationError as e:
        raise HTTPException(422, detail=str(e))
