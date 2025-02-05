from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.accounts.adapters.db.sql_model.merchant import SQLModelMerchantRepository
from app.accounts.adapters.db.sql_model.organization import (
    SQLModelOrganizationRepository,
)
from app.accounts.adapters.db.sql_model.user import SQLModelUserRepository
from app.accounts.services.auth_service import AuthService
from app.accounts.services.merchant_service import MerchantService
from app.accounts.services.organization_service import OrganizationService
from app.accounts.services.user_service import UserService
from app.common.adapters.cryptography.argon import Argon2PasswordHasher
from app.common.adapters.cryptography.jwt import JWTManager
from app.common.adapters.db.sql_model.session import get_session
from app.settings import Settings, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/auth/token")


@lru_cache
def get_settings():
    return settings


def get_password_hasher():
    """Create password hashing service.

    Returns:
        Configured BCryptPasswordHasher instance for password operations.
    """
    return Argon2PasswordHasher()


def get_auth_service(
    settings: Annotated[Settings, Depends(get_settings)],
    session: Session = Depends(get_session),
):
    """Create and configure the authentication service.

    Creates an AuthService instance with all required dependencies including
    user repository, password hasher, and token manager.

    Returns:
        Configured AuthService instance with 30-minute token expiration.
    """
    repo = SQLModelUserRepository(session=session)
    password_hasher = get_password_hasher()

    return AuthService(
        user_repo=repo,
        token_manager=get_token_manager(settings),
        password_hasher=password_hasher,
        access_token_expire_minutes=30,
    )


def get_user_service(session: Session = Depends(get_session)):
    """Create and configure the user service.

    Creates a UserService instance with all required dependencies including
    user repository.

    Returns:
        Configured UserService instance.
    """
    session = get_session()
    repo = SQLModelUserRepository(session=session)
    password_hasher = get_password_hasher()

    return UserService(
        user_repo=repo,
        password_hasher=password_hasher,
    )


def get_organization_service(session: Session = Depends(get_session)):
    """Create and configure the organization service.

    Returns:
        Configured OrganizationService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = SQLModelOrganizationRepository(session=session)
    return OrganizationService(repo)


def get_merchant_service(session: Session = Depends(get_session)):
    """Create and configure the merchant service.

    Returns:
        Configured MerchantService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = SQLModelMerchantRepository(session=session)
    return MerchantService(repo)


def get_token_manager(settings: Annotated[Settings, Depends(get_settings)]):
    """Create JWT token manager.

    Returns:
        Configured JWTManager instance for token operations.

    Note:
        Uses a hardcoded secret key - should be configured via environment
        variables in production.
    """
    return JWTManager(
        secret_key=settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )
