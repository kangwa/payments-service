"""Test fixtures specific to REST API endpoints."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.accounts.ports.rest.dependencies import (
    get_auth_service,
    get_user_service,
    get_merchant_service,
    get_organization_service
)
from app.accounts.ports.rest.router import accounts_router


@pytest.fixture
def app(mock_auth_service, mock_user_service, mock_merchant_service, mock_organization_service):
    """Test app fixture with dependency overrides."""
    app = FastAPI()
    app.include_router(accounts_router)

    app.dependency_overrides = {
        get_auth_service: lambda: mock_auth_service,
        get_user_service: lambda: mock_user_service,
        get_merchant_service: lambda: mock_merchant_service,
        get_organization_service: lambda: mock_organization_service,
    }
    return app

@pytest.fixture
def client(app):
    """Test client fixture."""
    return TestClient(app)

@pytest.fixture
def valid_token():
    """Valid JWT token for authentication."""
    return "valid.jwt.token"

@pytest.fixture
def auth_headers(valid_token):
    """Authorization headers with valid token."""
    return {"Authorization": f"Bearer {valid_token}"}

@pytest.fixture
def valid_login_data():
    """Valid login request data."""
    return {"email": "test@example.com", "password": "SecurePass123!"}

@pytest.fixture
def valid_register_data(valid_org_id):
    """Valid user registration data."""
    return {
        "email": "new@example.com",
        "password": "SecurePass123!",
        "organization_id": str(valid_org_id),
    }