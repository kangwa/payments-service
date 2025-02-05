"""Shared test fixtures for the accounts domain."""

from datetime import datetime, timedelta
from uuid import uuid4
from unittest.mock import Mock

import pytest

from app.accounts.entities.merchant import Merchant, MerchantStatus
from app.accounts.entities.organization import Organization, OrganizationStatus
from app.accounts.entities.user import User, UserStatus
from app.accounts.entities.token_data import TokenData
from app.accounts.schemas.user_schemas import UserResponse
from app.common.value_objects.email import Email
from app.common.value_objects.domain_name import DomainName


# Mock Services
@pytest.fixture
def mock_auth_service():
    """Mock authentication service."""
    return Mock()

@pytest.fixture
def mock_user_service():
    """Mock user service."""
    return Mock()

@pytest.fixture
def mock_organization_service():
    """Mock organization service."""
    return Mock()

@pytest.fixture
def mock_merchant_service():
    """Mock merchant service."""
    return Mock()

# Base Data
@pytest.fixture
def valid_org_id():
    """Fixture providing a consistent organization ID."""
    return uuid4()

@pytest.fixture
def valid_user_id():
    """Fixture providing a consistent user ID."""
    return uuid4()

@pytest.fixture
def valid_merchant_id():
    """Fixture providing a consistent merchant ID."""
    return uuid4()

@pytest.fixture
def valid_email() -> Email:
    """Fixture providing a valid Email value object."""
    return Email("test@example.com")

@pytest.fixture
def valid_domain() -> DomainName:
    """Fixture providing a valid domain name value object."""
    return DomainName("test-org.com")

# Organization Fixtures
@pytest.fixture
def valid_org_data():
    """Fixture providing valid organization test data."""
    return {
        "name": "Test Organization",
        "domain": "test-org.com",
        "status": OrganizationStatus.ACTIVE,
        "metadata": {},
    }

@pytest.fixture
def valid_organization(valid_org_data):
    """Fixture providing a valid Organization entity."""
    return Organization(**valid_org_data)

@pytest.fixture
def alternate_org_data():
    """Fixture providing alternate organization test data."""
    return {
        "id": uuid4(),
        "name": "Another Organization",
        "domain": "another-org.com",
        "status": OrganizationStatus.PENDING,
        "created_at": datetime(2024, 1, 2, 0, 0, 0),
        "updated_at": datetime(2024, 1, 2, 0, 0, 0),
        "metadata": {"type": "subsidiary"},
    }

# User Fixtures
@pytest.fixture
def valid_user_data(valid_org_id, valid_user_id, valid_email):
    """Fixture providing valid user test data."""
    return {
        "id": valid_user_id,
        "email": valid_email,
        "organization_id": valid_org_id,
        "hashed_password": "hashed_secret_password_123",
        "name": "Test User",
        "status": UserStatus.ACTIVE,
        "created_at": datetime(2024, 1, 1, 0, 0, 0),
        "last_login": None,
    }

@pytest.fixture
def valid_user(valid_user_data):
    """Fixture providing a valid User entity."""
    return User(**valid_user_data)

@pytest.fixture
def alternate_user_data(alternate_org_data):
    """Fixture providing alternate user test data."""
    return {
        "id": uuid4(),
        "email": Email("another.user@another-org.com"),
        "organization_id": alternate_org_data["id"],
        "hashed_password": "different_hashed_password_456",
        "name": "Another User",
        "status": UserStatus.ACTIVE,
        "created_at": datetime(2024, 1, 2, 0, 0, 0),
        "last_login": datetime(2024, 1, 2, 1, 0, 0),
    }

# Merchant Fixtures
@pytest.fixture
def valid_merchant_request_data(valid_org_id, valid_merchant_id):
    """Fixture providing valid merchant test data."""
    return {
        "organization_id": str(valid_org_id),
        "name": "Test Merchant",
        "description": "Test merchant description",
        "country_code": "US",
        "currency": "USD",
        "status": MerchantStatus.ACTIVE,
        "payment_methods": [],
        "api_keys": [],
        "metadata": {},
    }

@pytest.fixture
def valid_merchant(valid_merchant_request_data):
    """Fixture providing a valid Merchant entity."""
    return Merchant(**valid_merchant_request_data)

@pytest.fixture
def valid_merchant_response_data(valid_merchant_id):
    """Fixture providing valid merchant response data."""
    return {
        "id": valid_merchant_id,
        "name": "Test Merchant",
        "country_code": "US",
        "currency": "USD",
        "status": "active",
    }

# Token Fixtures
@pytest.fixture
def valid_token(valid_user):
    """Fixture providing valid token test data."""
    return TokenData.create_token(
        user_id=valid_user.id,
        email=valid_user.email,
        expires_in=timedelta(hours=1)
    )

# Response Model Fixtures
@pytest.fixture
def valid_user_response_data(valid_user_data):
    """Fixture providing valid user response data."""
    return {
        "id": valid_user_data["id"],
        "email": valid_user_data["email"],
        "status": valid_user_data["status"],
        "organization_id": valid_user_data["organization_id"],
        "created_at": valid_user_data["created_at"],
        "last_login": valid_user_data["last_login"],
    }

@pytest.fixture
def valid_user_response(valid_user_response_data):
    """Fixture providing valid user response."""
    return UserResponse(**valid_user_response_data)

# Utility Fixtures
@pytest.fixture
def mock_datetime(monkeypatch):
    """Fixture to mock datetime for consistent timestamps."""
    class MockDateTime:
        @staticmethod
        def now():
            return datetime(2024, 1, 1, 0, 0, 0)

    monkeypatch.setattr("app.accounts.entities.organization.datetime", MockDateTime)
    monkeypatch.setattr("app.accounts.entities.user.datetime", MockDateTime)
    monkeypatch.setattr("app.accounts.entities.merchant.datetime", MockDateTime)
    return MockDateTime


@pytest.fixture
def user(valid_user_data):
    """Fixture providing a valid User instance."""
    return User(**valid_user_data)