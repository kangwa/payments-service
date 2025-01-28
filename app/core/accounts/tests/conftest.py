import pytest
from faker import Faker

from app.core.accounts.models import Organization, Merchant

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
