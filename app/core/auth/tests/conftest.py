from datetime import timedelta
import pytest
from faker import Faker

from app.core.auth.models import TokenData, User

fake = Faker()


@pytest.fixture
def user():
    """Fixture providing a basic user instance for testing."""
    return User(email="test@example.com", hashed_password="hashed_secret")


@pytest.fixture
def token_data(user):
    """Fixture providing a token data instance for testing."""
    return TokenData.create_token(user=user, expires_in=timedelta(hours=1))
