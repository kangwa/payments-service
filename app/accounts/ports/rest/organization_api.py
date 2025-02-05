from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.accounts.ports.rest.dependencies import get_organization_service
from app.accounts.schemas.organization_schemas import (
    OrganizationCreateRequest,
    OrganizationListResponse,
    OrganizationResponse,
)
from app.accounts.services.organization_service import OrganizationService
from app.common.exceptions import ValidationError

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/", response_model=OrganizationListResponse)
def list_organizations(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: str = Query(None),
    service: OrganizationService = Depends(get_organization_service),
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
        organizations, total = service.list_organizations(
            limit=limit, offset=offset, status=status
        )

        return {"data": organizations, "total": total, "limit": limit, "offset": offset}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    data: OrganizationCreateRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    """Create a new organization.

    Creates an organization with the specified name and default status.

    Args:
        data: Organization creation data containing name.
        service: Injectable organization service instance.

    Returns:
        OrganizationResponse containing the created organization's details.

    Raises:
        HTTPException(400): If organization creation fails due to invalid data
            or business rule violations.

    Example:
        ```
        POST /organizations/
        {
            "name": "Acme Corporation"
        }
        ```
    """
    try:
        return service.create_organization(name=data.name, domain=data.domain)
    except ValidationError as e:
        raise HTTPException(422, detail=str(e))


@router.post("/{org_id}/suspend", response_model=OrganizationResponse)
def suspend_organization(
    org_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    """Suspend an active organization.

    Changes the status of an organization to suspended. This operation
    may affect associated resources and permissions.

    Args:
        org_id: UUID of the organization to suspend.
        service: Injectable organization service instance.

    Returns:
        OrganizationResponse containing the updated organization details.

    Raises:
        HTTPException(404): If organization is not found.
        HTTPException(400): If organization cannot be suspended in its current state.

    Example:
        ```
        POST /organizations/123e4567-e89b-12d3-a456-426614174000/suspend
        ```
    """
    try:
        return service.suspend_organization(org_id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(
    org_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
):
    """Get an organization."""
    try:
        return service.get_organization(org_id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
