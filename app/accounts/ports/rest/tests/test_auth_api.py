"""Test suite for authentication API endpoints."""

from unittest.mock import patch
from uuid import UUID

from app.accounts.exceptions import AuthenticationError
from app.common.exceptions import ValidationError


class TestAuthAPI:
    """Test cases for authentication endpoints."""

    def test_register_user_success(
        self, client, mock_user_service, valid_register_data, valid_user
    ):
        """Test successful user registration."""
        # Setup
        mock_user_service.create_user.return_value = valid_user

        # Execute
        response = client.post("/accounts/auth/register", json=valid_register_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"]["value"] == str(valid_user.email)
        assert "password" not in data

        # Verify service call
        mock_user_service.create_user.assert_called_once_with(
            email_address=valid_register_data["email"],
            plain_password=valid_register_data["password"],
            organization_id=UUID(valid_register_data["organization_id"]),
        )

    def test_register_user_already_exists(
        self, client, mock_user_service, valid_register_data
    ):
        """Test registration with existing email."""
        # Setup
        mock_user_service.create_user.side_effect = ValidationError(
            "User already exists"
        )

        # Execute
        response = client.post("/accounts/auth/register", json=valid_register_data)

        # Assert
        assert response.status_code == 422
        assert "already exists" in response.json()["detail"]

    def test_register_validation_error(self, client):
        """Test registration with invalid data."""
        # Execute
        response = client.post(
            "/accounts/auth/register",
            json={
                "email": "invalid-email",
                "password": "short",
                "organization_id": "invalid-uuid",
            },
        )

        # Assert
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert len(errors) > 0

    def test_oauth_token_success(
        self, client, mock_auth_service, valid_user, valid_login_data
    ):
        """Test successful OAuth2 token request."""
        with patch(
            "app.accounts.ports.rest.dependencies.get_auth_service",
            return_value=mock_auth_service,
        ):
            # Setup
            mock_auth_service.authenticate_user.return_value = valid_user
            mock_auth_service.create_access_token.return_value = "test.jwt.token"

            # Execute
            response = client.post(
                "/accounts/auth/token",
                data={
                    "username": valid_login_data["email"],
                    "password": valid_login_data["password"],
                    "grant_type": "password",
                },
            )

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "test.jwt.token"
            assert data["token_type"] == "bearer"

    def test_oauth_token_invalid_credentials(
        self, client, mock_auth_service, valid_login_data
    ):
        """Test OAuth2 token with invalid credentials."""
        # Setup
        mock_auth_service.authenticate_user.side_effect = AuthenticationError(
            "Invalid credentials"
        )

        # Execute
        response = client.post(
            "/accounts/auth/token",
            data={
                "username": valid_login_data["email"],
                "password": valid_login_data["password"],
                "grant_type": "password",
            },
        )

        # Assert
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
