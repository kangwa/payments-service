from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.auth.exceptions import AuthenticationError
from app.core.auth.adapters.db.in_memory import InMemoryUserRepository
from app.core.auth.models import User
from app.core.auth.services.auth_service import AuthService
from app.core.auth.adapters.cryptography.bcrypt import BCryptPasswordHasher
from app.core.auth.adapters.cryptography.jwt import JWTManager
from app.core.auth.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hasher():
    """Create password hashing service.

    Returns:
        Configured BCryptPasswordHasher instance for password operations.
    """
    return BCryptPasswordHasher()


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


def get_user_service():
    """Create and configure the user service.

    Creates a UserService instance with all required dependencies including
    user repository.

    Returns:
        Configured UserService instance.
    """
    repo = InMemoryUserRepository()
    password_hasher = get_password_hasher()

    return UserService(
        user_repo=repo,
        password_hasher=password_hasher,
    )


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


def get_token_manager():
    """Create JWT token manager.

    Returns:
        Configured JWTManager instance for token operations.

    Note:
        Uses a hardcoded secret key - should be configured via environment
        variables in production.
    """
    return JWTManager(secret_key="your-secret-key-here", algorithm="HS256")
