"""Service test fixtures."""

from unittest.mock import Mock

import pytest

from app.accounts.interfaces.merchant_repo import MerchantRepository
from app.accounts.interfaces.organization_repo import OrganizationRepository
from app.accounts.interfaces.user_repo import UserRepository
from app.common.interfaces.password_hasher import PasswordHasher
from app.common.interfaces.token_manager import TokenManager


@pytest.fixture
def mock_merchant_repo():
    """Mock merchant repository."""
    repo = Mock(spec=MerchantRepository)
    repo.list_all.return_value = []
    repo.count.return_value = 0
    return repo


@pytest.fixture
def mock_organization_repo():
    """Mock organization repository."""
    repo = Mock(spec=OrganizationRepository)
    repo.list_all.return_value = []
    repo.count.return_value = 0
    return repo


@pytest.fixture
def mock_user_repo():
    """Mock user repository."""
    repo = Mock(spec=UserRepository)
    repo.list_all.return_value = []
    repo.count.return_value = 0
    return repo


@pytest.fixture
def mock_password_hasher():
    """Mock password hasher."""
    hasher = Mock(spec=PasswordHasher)
    hasher.hash.return_value = "hashed_password"
    hasher.verify.return_value = True
    return hasher


@pytest.fixture
def mock_token_manager():
    """Mock token manager."""
    manager = Mock(spec=TokenManager)
    manager.create_access_token.return_value = "test_token"
    return manager
