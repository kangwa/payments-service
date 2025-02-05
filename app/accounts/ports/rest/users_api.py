from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.accounts.ports.rest.dependencies import get_user_service
from app.accounts.schemas.user_schemas import UserListResponse, UserResponse
from app.accounts.services.user_service import UserService

router = APIRouter()
router = APIRouter(prefix="/organizations/{org_id}/users", tags=["Users"])


@router.get("/", response_model=UserListResponse)
def list_users(
    org_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: str = Query(None),
    service: UserService = Depends(get_user_service),
):
    """List users with pagination and optional status filtering."""
    try:
        users, total = service.list_users(
            org_id,
            limit=limit,
            offset=offset,
            status=status,
        )

        return {
            "data": users,
            "total": total,
            "limit": limit,
            "offset": offset,
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    """Get a user."""
    try:
        return user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
