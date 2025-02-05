"""Test suite for authentication schemas."""

import pytest
from pydantic import ValidationError

from app.accounts.schemas.auth_schemas import LoginRequest, TokenResponse


class TestLoginRequest:
    """Test cases for LoginRequest schema."""

    def test_valid_login_request(self):
        """Test creating login request with valid data."""
        data = {"email": "test@example.com", "password": "SecurePass123!"}
        request = LoginRequest(**data)
        assert request.email == "test@example.com"
        assert request.password == "SecurePass123!"

    def test_invalid_email_format(self):
        """Test validation of invalid email format."""
        with pytest.raises(ValidationError) as exc:
            LoginRequest(email="invalid-email", password="SecurePass123!")

        errors = exc.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "value_error"
        assert "email" in errors[0]["loc"]

    def test_password_too_short(self):
        """Test validation of short password."""
        with pytest.raises(ValidationError) as exc:
            LoginRequest(email="test@example.com", password="short")

        errors = exc.value.errors()
        assert len(errors) == 1
        assert errors[0]["type"] == "string_too_short"
        assert "password" in errors[0]["loc"]

    def test_missing_fields(self):
        """Test validation of missing required fields."""
        with pytest.raises(ValidationError) as exc:
            LoginRequest()

        errors = exc.value.errors()
        assert len(errors) == 2
        assert {"email", "password"} == {e["loc"][0] for e in errors}


class TestTokenResponse:
    """Test cases for TokenResponse schema."""

    def test_valid_token_response(self):
        """Test creating token response with valid data."""
        data = {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...", "token_type": "bearer"}
        response = TokenResponse(**data)
        assert response.access_token == data["access_token"]
        assert response.token_type == "bearer"

    def test_default_token_type(self):
        """Test default token_type value."""
        response = TokenResponse(access_token="test-token")
        assert response.token_type == "bearer"

    def test_missing_access_token(self):
        """Test validation of missing access token."""
        with pytest.raises(ValidationError) as exc:
            TokenResponse(token_type="bearer")

        errors = exc.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"][0] == "access_token"

    def test_json_serialization(self):
        """Test JSON serialization of token response."""
        response = TokenResponse(access_token="test-token", token_type="bearer")
        json_data = response.model_dump_json()
        assert all(field in json_data for field in ["access_token", "token_type"])
