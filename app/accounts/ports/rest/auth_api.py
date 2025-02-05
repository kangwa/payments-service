"""Authentication endpoints for the accounts domain.

This module provides REST API endpoints for user authentication operations,
including login, registration, and token management. All endpoints follow
OAuth2 standards with JWT tokens for authentication.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.accounts.exceptions import AuthenticationError, UserNotFoundError
from app.accounts.ports.rest.dependencies import get_auth_service, get_user_service
from app.accounts.schemas.auth_schemas import TokenResponse
from app.accounts.schemas.user_schemas import UserCreateRequest, UserResponse
from app.accounts.services.auth_service import AuthService
from app.accounts.services.user_service import UserService
from app.common.exceptions import ValidationError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=TokenResponse,
    responses={401: {"description": "Invalid credentials"}},
)
def oauth_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
):
    """OAuth2 compatible token endpoint.

    Standard OAuth2 token endpoint that accepts form-encoded credentials
    and returns a JWT token.

    Args:
        form_data: OAuth2 password grant credentials.
        auth_service: Injectable authentication service.

    Returns:
        JWT access token response.

    Raises:
        HTTPException(401): If credentials are invalid.

    Note:
        This endpoint is compatible with standard OAuth2 clients.
    """
    try:
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        token = auth_service.create_access_token(user)
        return TokenResponse(access_token=token, token_type="bearer")

    except (UserNotFoundError, AuthenticationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "User already exists"},
        422: {"description": "Validation error"},
    },
)
def register_user(
    request: UserCreateRequest,
    user_service: UserService = Depends(get_user_service),
):
    """Register a new user account.

    Creates a new user account with the provided email and password.
    The password must meet the security requirements.

    Args:
        request: User registration data.
        user_service: Injectable user service.

    Returns:
        Created user profile.

    Raises:
        HTTPException(400): If user already exists.
        HTTPException(422): If validation fails.

    Example:
        ```http
        POST /auth/register
        {
            "email": "new@example.com",
            "password": "SecurePass123!",
            "organization_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
    """
    try:
        user = user_service.create_user(
            email_address=request.email,
            plain_password=request.password,
            organization_id=request.organization_id,
        )
        return UserResponse.model_validate(user)

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
