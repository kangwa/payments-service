from datetime import datetime
from uuid import UUID

import pytest

from app.accounts.entities.user import User, UserStatus
from app.common.value_objects.email import Email


class TestUser:
    """Test suite for User entity."""

    def test_create_user_with_valid_data(self, valid_user_data):
        """Test user creation with valid data."""
        user = User(**valid_user_data)

        assert isinstance(user.id, UUID)
        assert isinstance(user.email, Email)
        assert user.email.value == valid_user_data["email"].value
        assert user.organization_id == valid_user_data["organization_id"]
        assert user.hashed_password == valid_user_data["hashed_password"]
        assert user.name == valid_user_data["name"]
        assert user.status == UserStatus.ACTIVE
        assert isinstance(user.created_at, datetime)
        assert user.last_login is None

    def test_name_validation(self, valid_user_data):
        """Test name validation rules."""
        # Test empty string
        with pytest.raises(ValueError, match="Name cannot be empty string"):
            valid_user_data["name"] = "   "
            User(**valid_user_data)

        # Test None is allowed
        valid_user_data["name"] = None
        user = User(**valid_user_data)
        assert user.name is None

        # Test whitespace is stripped
        valid_user_data["name"] = "  Test User  "
        user = User(**valid_user_data)
        assert user.name == "Test User"

    def test_status_transitions(self, valid_user):
        """Test user status transition methods."""
        assert valid_user.status == UserStatus.ACTIVE

        valid_user.deactivate()
        assert valid_user.status == UserStatus.INACTIVE

        valid_user.suspend()
        assert valid_user.status == UserStatus.SUSPENDED

        valid_user.activate()
        assert valid_user.status == UserStatus.ACTIVE

    def test_record_login(self, valid_user):
        """Test login recording functionality."""
        assert valid_user.last_login is None

        valid_user.record_login()
        assert isinstance(valid_user.last_login, datetime)

    def test_is_active_property(self, valid_user):
        """Test is_active property behavior."""
        assert valid_user.is_active is True

        valid_user.deactivate()
        assert valid_user.is_active is False

        valid_user.suspend()
        assert valid_user.is_active is False

        valid_user.activate()
        assert valid_user.is_active is True
