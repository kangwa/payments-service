"""Test suite for user schemas."""

from datetime import datetime
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from app.accounts.entities.user import UserStatus
from app.accounts.schemas.user_schemas import (
    UserCreateRequest,
    UserListResponse,
    UserLoginRequest,
    UserResponse,
)
from app.common.value_objects.email import Email


class TestUserCreateRequest:
    """Test cases for UserCreateRequest schema."""

    def test_valid_create_request(self):
        """Test creating request with valid data."""
        org_id = uuid4()
        data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "organization_id": str(org_id),
        }
        request = UserCreateRequest(**data)
        assert request.email == "test@example.com"
        assert request.password == "SecurePass123!"
        assert request.organization_id == org_id

    def test_invalid_email(self):
        """Test validation of invalid email."""
        with pytest.raises(ValidationError) as exc:
            UserCreateRequest(
                email="invalid-email",
                password="SecurePass123!",
                organization_id=str(uuid4()),
            )
        assert "email" in str(exc.value)

    def test_invalid_org_id(self):
        """Test validation of invalid organization ID."""
        with pytest.raises(ValidationError) as exc:
            UserCreateRequest(
                email="test@example.com",
                password="SecurePass123!",
                organization_id="invalid-uuid",
            )
        assert "organization_id" in str(exc.value)


class TestUserLoginRequest:
    """Test cases for UserLoginRequest schema."""

    def test_valid_login_request(self):
        """Test creating login request with valid data."""
        data = {"email": "test@example.com", "password": "SecurePass123!"}
        request = UserLoginRequest(**data)
        assert request.email == "test@example.com"
        assert request.password == "SecurePass123!"

    def test_missing_fields(self):
        """Test validation of missing required fields."""
        with pytest.raises(ValidationError) as exc:
            UserLoginRequest()
        errors = exc.value.errors()
        assert len(errors) == 2
        assert {"email", "password"} == {e["loc"][0] for e in errors}


class TestUserResponse:
    """Test cases for UserResponse schema."""

    def test_valid_user_response(self, valid_user_data):
        """Test creating response with valid data."""
        response = UserResponse(**valid_user_data)
        assert isinstance(response.id, UUID)
        assert isinstance(response.email, Email)
        assert response.status == UserStatus.ACTIVE
        assert isinstance(response.organization_id, UUID)
        assert isinstance(response.created_at, datetime)
        assert response.last_login is None

    def test_json_serialization(self, valid_user_response_data):
        """Test JSON serialization of user response."""
        response = UserResponse(**valid_user_response_data)
        json_data = response.model_dump_json()
        assert all(
            field in json_data
            for field in ["id", "email", "status", "organization_id", "created_at"]
        )


class TestUserListResponse:
    """Test cases for UserListResponse schema."""

    def test_valid_list_response(self, valid_user_response):
        """Test creating list response with valid data."""
        data = {"data": [valid_user_response], "total": 1, "limit": 10, "offset": 0}
        response = UserListResponse(**data)
        assert len(response.data) == 1
        assert response.total == 1
        assert response.limit == 10
        assert response.offset == 0

    def test_invalid_pagination_values(self, valid_user_response):
        """Test validation of invalid pagination values."""
        with pytest.raises(ValidationError):
            UserListResponse(
                data=[valid_user_response],
                total=-1,  # Invalid negative value
                limit=10,
                offset=0,
            )

        with pytest.raises(ValidationError):
            UserListResponse(
                data=[valid_user_response],
                total=1,
                limit=0,  # Invalid zero value
                offset=0,
            )
