"""Test suite for AuthService."""

from datetime import timedelta
from unittest.mock import Mock

import pytest

from app.accounts.entities.user import UserStatus
from app.accounts.exceptions import (
    AuthenticationError,
    InactiveUserError,
    UserNotFoundError,
)
from app.accounts.services.auth_service import AuthService


class TestAuthService:
    """Test cases for AuthService."""

    @pytest.fixture
    def mock_user_repo(self):
        """Mock user repository fixture."""
        return Mock()

    @pytest.fixture
    def mock_password_hasher(self):
        """Mock password hasher fixture."""
        return Mock()

    @pytest.fixture
    def mock_token_manager(self):
        """Mock token manager fixture."""
        return Mock()

    @pytest.fixture
    def auth_service(self, mock_user_repo, mock_password_hasher, mock_token_manager):
        """Auth service fixture."""
        return AuthService(
            user_repo=mock_user_repo,
            password_hasher=mock_password_hasher,
            token_manager=mock_token_manager,
            access_token_expire_minutes=30,
        )

    def test_authenticate_user_success(
        self, auth_service, mock_user_repo, mock_password_hasher, valid_user
    ):
        """Test successful user authentication."""
        # Setup
        mock_user_repo.get_by_email.return_value = valid_user
        mock_password_hasher.verify.return_value = True

        # Execute
        user = auth_service.authenticate_user(
            email=str(valid_user.email), password="correct_password"
        )

        # Assert
        assert user == valid_user
        mock_user_repo.get_by_email.assert_called_once_with(str(valid_user.email))
        mock_password_hasher.verify.assert_called_once_with(
            "correct_password", valid_user.hashed_password
        )

    def test_authenticate_user_invalid_credentials(
        self, auth_service, mock_user_repo, mock_password_hasher, valid_user
    ):
        """Test authentication with invalid credentials."""
        # Setup
        mock_user_repo.get_by_email.return_value = valid_user
        mock_password_hasher.verify.return_value = False

        # Execute and Assert
        with pytest.raises(AuthenticationError, match="Invalid email or password"):
            auth_service.authenticate_user(
                email=str(valid_user.email), password="wrong_password"
            )

    def test_authenticate_inactive_user(
        self, auth_service, mock_user_repo, mock_password_hasher, valid_user
    ):
        """Test authentication of inactive user."""
        # Setup
        valid_user.status = UserStatus.INACTIVE
        mock_user_repo.get_by_email.return_value = valid_user
        mock_password_hasher.verify.return_value = True

        # Execute and Assert
        with pytest.raises(InactiveUserError, match="User account is not active"):
            auth_service.authenticate_user(
                email=str(valid_user.email), password="password"
            )

    def test_create_access_token_success(
        self, auth_service, mock_token_manager, valid_user
    ):
        """Test successful access token creation."""
        # Setup
        expected_token = "jwt_token"
        mock_token_manager.create_access_token.return_value = expected_token

        # Execute
        token = auth_service.create_access_token(valid_user)

        # Assert
        assert token == expected_token
        mock_token_manager.create_access_token.assert_called_once()
        call_args = mock_token_manager.create_access_token.call_args[1]
        assert call_args["data"]["user_id"] == str(valid_user.id)
        assert call_args["data"]["email"] == str(valid_user.email)
        assert isinstance(call_args["expires_delta"], timedelta)

    def test_authenticate_user_not_found(
        self,
        auth_service,
        mock_user_repo,
    ):
        """Test authentication with non-existent user."""
        # Setup
        mock_user_repo.get_by_email.return_value = None

        # Execute and Assert
        with pytest.raises(
            UserNotFoundError, match="User with email test@example.com not found"
        ):
            auth_service.authenticate_user(
                email="test@example.com", password="any_password"
            )

    def test_authenticate_user_wrong_password(
        self, auth_service, mock_user_repo, mock_password_hasher, valid_user
    ):
        """Test authentication with wrong password."""
        # Setup
        mock_user_repo.get_by_email.return_value = valid_user
        mock_password_hasher.verify.return_value = False

        # Execute and Assert
        with pytest.raises(AuthenticationError, match="Invalid email or password"):
            auth_service.authenticate_user(
                email=str(valid_user.email), password="wrong_password"
            )
