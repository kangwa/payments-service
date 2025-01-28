from datetime import datetime, timedelta
from uuid import UUID
from freezegun import freeze_time

from app.core.auth.models import TokenData, UserStatus


def test_user_initialization(user):
    """Test that user is initialized with correct default values.

    Verifies:
    - Required fields are set correctly
    - Optional fields have correct default values
    - Status starts as ACTIVE
    """
    assert isinstance(user.user_id, UUID)
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_secret"
    assert user.status == UserStatus.ACTIVE
    assert isinstance(user.created_at, datetime)
    assert user.last_login is None


def test_user_status_changes(user):
    """Test user status transition methods.

    Verifies:
    - Status changes work correctly
    - is_active property reflects current status
    """
    assert user.is_active is True

    user.deactivate()
    assert user.status == UserStatus.INACTIVE
    assert user.is_active is False

    user.activate()
    assert user.status == UserStatus.ACTIVE
    assert user.is_active is True

    user.suspend()
    assert user.status == UserStatus.SUSPENDED
    assert user.is_active is False


@freeze_time("2024-01-23 12:00:00")
def test_login_recording(user):
    """Test login timestamp recording.

    Verifies:
    - Last login timestamp is updated correctly
    """
    assert user.last_login is None

    user.record_login()
    assert user.last_login == datetime.now()


def test_token_creation(user):
    """Test token creation from user data.

    Verifies:
    - Token is created with correct user data
    - Expiration time is set correctly
    """
    token = TokenData.create_token(user=user, expires_in=timedelta(hours=1))

    assert token.user_id == user.user_id
    assert token.email == user.email
    assert isinstance(token.expires_at, datetime)


@freeze_time("2024-01-23 12:00:00")
def test_token_expiration(user):
    """Test token expiration checking.

    Verifies:
    - Token expiration is correctly determined
    - is_expired property works as expected
    """
    token_ttl = timedelta(minutes=60)
    token = TokenData.create_token(user=user, expires_in=token_ttl)

    assert token.is_expired is False

    with freeze_time("2024-01-23 13:01:00"):  # 1 hour and 1 minute later
        assert token.is_expired is True
