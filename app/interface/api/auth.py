from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.application.commands.auth_commands import CreateUserCommand
from app.application.services.auth_service import AuthService
from app.domain.models.auth import User
from app.interface.api.dependencies import get_auth_service, get_current_user as get_me
from app.interface.schemas.auth import UserCreateRequest, UserResponse


router = APIRouter(tags=["Authentication"])


class TokenResponse(BaseModel):
    """Schema for API authentication token response.

    Attributes:
        access_token: The JWT access token for authentication.
        token_type: The type of token (always "bearer").
    """

    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserCreateRequest,  # Reuses create schema for login
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate user and generate access token.

    Args:
        request: User credentials containing email and password.
        auth_service: Injectable authentication service.

    Returns:
        TokenResponse containing JWT access token.

    Raises:
        HTTPException(401): If credentials are invalid.

    Note:
        This endpoint reuses the UserCreateRequest schema for simplicity,
        though only email and password fields are used.
    """
    user = await auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = auth_service.create_access_token(user)
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_me)):
    """Get the currently authenticated user's details.

    Args:
        current_user: User object from JWT token validation dependency.

    Returns:
        Complete user object for authenticated user.

    Note:
        This endpoint requires a valid JWT token in the Authorization header.
        Authentication is handled by the get_current_user dependency.
    """
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: UserCreateRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Register a new user.

    Args:
        request: User registration data containing email and password.
        auth_service: Injectable authentication service.

    Returns:
        UserResponse containing the created user's details.

    Raises:
        HTTPException(400): If user already exists or data is invalid.

    Note:
        Password requirements and validation are handled by the UserCreateRequest schema.
        The response excludes sensitive fields like hashed_password.
    """
    try:
        user = await auth_service.create_user(
            CreateUserCommand(email=request.email, password=request.password)
        )
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            status=user.status,
            created_at=user.created_at,
            last_login=user.last_login,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
):
    print(form_data.username, form_data.password)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = auth_service.create_access_token(user)
    return TokenResponse(access_token=token, token_type="bearer")
