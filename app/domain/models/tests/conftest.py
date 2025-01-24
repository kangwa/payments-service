from datetime import timedelta
import pytest
from faker import Faker

from app.domain.models.api_key import ApiKey
from app.domain.models.auth import TokenData, User
from app.domain.models.merchant import Merchant
from app.domain.models.organization import Organization

fake = Faker()


@pytest.fixture
def org():
    """Fixture providing a basic organization instance for testing."""
    return Organization(name=fake.company())


@pytest.fixture
def merchant(org):
    """Fixture providing a basic merchant instance for testing.

    Returns a merchant with minimal required fields set.
    """
    return Merchant(
        organization_id=org.id,
        name=fake.company(),
        country_code=fake.country_code(),
        currency=fake.currency_code(),
    )


@pytest.fixture
def user():
    """Fixture providing a basic user instance for testing."""
    return User(email="test@example.com", hashed_password="hashed_secret")


@pytest.fixture
def token_data(user):
    """Fixture providing a token data instance for testing."""
    return TokenData.create_token(user=user, expires_in=timedelta(hours=1))


# Tests
import pytest


@pytest.fixture
def api_key(merchant):
    """Fixture providing a basic API key instance for testing."""
    return ApiKey(
        merchant_id=merchant.id,
        name="Test Key",
        description="Test key for unit tests",
        hashed_key="hashed_secret",
        key_prefix="test_",
    )
