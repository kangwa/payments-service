"""Test suite for TokenData entity."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.accounts.entities.token_data import TokenData
from app.common.value_objects.email import Email


class TestTokenData:
    """Test suite for TokenData entity."""

    def test_create_token_data_with_valid_data(self, valid_token, valid_user):
        """Test token creation with valid data."""
        assert valid_token.user_id == valid_user.id
        assert isinstance(valid_token.email, Email)
        assert str(valid_token.email) == str(valid_user.email)
        assert isinstance(valid_token.expires_at, datetime)

    def test_create_token_class_method(self, valid_email):
        """Test token creation via class method."""
        user_id = uuid4()
        expires_in = timedelta(hours=1)

        token = TokenData.create_token(
            user_id=user_id, email=valid_email, expires_in=expires_in
        )

        assert token.user_id == user_id
        assert token.email == valid_email
        assert isinstance(token.expires_at, datetime)
        assert not token.is_expired

        # Verify expiration time is set correctly
        expected_expiry = datetime.now() + expires_in
        difference = abs((token.expires_at - expected_expiry).total_seconds())
        assert difference < 1  # Allow 1 second tolerance

    def test_is_expired_property(self, valid_email):
        """Test is_expired property behavior."""
        user_id = uuid4()

        # Test non-expired token
        token = TokenData.create_token(
            user_id=user_id, email=valid_email, expires_in=timedelta(hours=1)
        )
        assert not token.is_expired

        # Test expired token
        token = TokenData(
            user_id=user_id,
            email=valid_email,
            expires_at=datetime.now() - timedelta(minutes=1),
        )
        assert token.is_expired

    def test_json_serialization(self, valid_token):
        """Test JSON serialization of token with Email value object."""
        json_data = valid_token.model_dump_json()

        assert "email" in json_data
        assert "user_id" in json_data

    def test_invalid_email_type(self, valid_user_data):
        """Test token creation with invalid email type."""
        valid_user_data["email"] = "test@example.com"  # str instead of Email

        with pytest.raises(ValueError):
            TokenData(**valid_user_data)
