from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.application.services.auth_service import AuthService
from app.application.services.merchant_service import MerchantService
from app.application.services.organization_service import OrganizationService
from app.domain.models.auth import User
from app.exceptions import AuthenticationError
from app.infrastructure.auth.bcrypt import BCryptPasswordHasher
from app.infrastructure.auth.jwt import JWTManager
from app.infrastructure.repositories.in_memory.merchant_repo import (
    InMemoryMerchantRepository,
)
from app.infrastructure.repositories.in_memory.organization_repo import (
    InMemoryOrganizationRepository,
)
from app.infrastructure.repositories.in_memory.user_repo import InMemoryUserRepository


async def get_organization_service():
    """Create and configure the organization service.

    Returns:
        Configured OrganizationService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = InMemoryOrganizationRepository()
    return OrganizationService(repo)


async def get_merchant_service():
    """Create and configure the merchant service.

    Returns:
        Configured MerchantService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = InMemoryMerchantRepository()
    return MerchantService(repo)


def get_password_hasher():
    """Create password hashing service.

    Returns:
        Configured BCryptPasswordHasher instance for password operations.
    """
    return BCryptPasswordHasher()


def get_token_manager():
    """Create JWT token manager.

    Returns:
        Configured JWTManager instance for token operations.

    Note:
        Uses a hardcoded secret key - should be configured via environment
        variables in production.
    """
    return JWTManager(secret_key="your-secret-key-here", algorithm="HS256")


def get_auth_service():
    """Create and configure the authentication service.

    Creates an AuthService instance with all required dependencies including
    user repository, password hasher, and token manager.

    Returns:
        Configured AuthService instance with 30-minute token expiration.
    """
    repo = InMemoryUserRepository()
    password_hasher = get_password_hasher()

    return AuthService(
        user_repo=repo,
        token_manager=get_token_manager(),
        password_hasher=password_hasher,
        access_token_expire_minutes=30,
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """FastAPI dependency for getting the current authenticated user.

    Validates the JWT token and retrieves the corresponding user.

    Args:
        token: JWT token from Authorization header (injected by oauth2_scheme).
        auth_service: Authentication service instance (injected by FastAPI).

    Returns:
        Authenticated User instance.

    Raises:
        HTTPException(401): If token is invalid or authentication fails.

    Note:
        This dependency can be used to protect endpoints requiring authentication:
        ```python
        @router.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"message": f"Hello {user.email}"}
        ```
    """
    try:
        return await auth_service.get_current_user(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
