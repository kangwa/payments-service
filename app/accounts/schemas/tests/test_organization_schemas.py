"""Test suite for organization schemas."""

from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.accounts.schemas.organization_schemas import (
    OrganizationCreateRequest,
    OrganizationListResponse,
    OrganizationResponse,
)


class TestOrganizationCreateRequest:
    """Test cases for OrganizationCreateRequest schema."""

    def test_valid_create_request(self):
        """Test creating request with valid data."""
        data = {"name": "Acme Corporation", "domain": "acme.com"}
        request = OrganizationCreateRequest(**data)
        assert request.name == data["name"]
        assert request.domain == data["domain"]

    def test_name_validation(self):
        """Test name field validation rules."""
        # Test empty name
        with pytest.raises(ValidationError) as exc:
            OrganizationCreateRequest(name="", domain="acme.com")
        assert "name" in str(exc.value)

        # Test too long name
        with pytest.raises(ValidationError) as exc:
            OrganizationCreateRequest(
                name="A" * 101, domain="acme.com"  # Exceeds max length
            )
        assert "name" in str(exc.value)


class TestOrganizationResponse:
    """Test cases for OrganizationResponse schema."""

    def test_valid_response(self, valid_organization):
        """Test creating response with valid data."""
        response = OrganizationResponse.model_validate(valid_organization)
        assert isinstance(response.id, UUID)
        assert response.name == valid_organization.name
        assert response.status == valid_organization.status
        assert isinstance(response.created_at, datetime)

    def test_json_serialization(self, valid_organization):
        """Test JSON serialization of organization response."""
        json_data = valid_organization.model_dump_json()
        assert all(
            field in json_data for field in ["id", "name", "status", "created_at"]
        )

    def test_from_attributes_config(self, valid_organization):
        """Test from_attributes configuration."""
        response = OrganizationResponse.model_validate(valid_organization)
        assert response.id == valid_organization.id
        assert response.name == valid_organization.name


class TestOrganizationListResponse:
    """Test cases for OrganizationListResponse schema."""

    @pytest.fixture
    def valid_org_response(self, valid_organization):
        """Fixture providing valid organization response."""
        return OrganizationResponse.model_validate(valid_organization)

    def test_valid_list_response(self, valid_org_response):
        """Test creating list response with valid data."""
        data = {"data": [valid_org_response], "total": 1, "limit": 10, "offset": 0}
        response = OrganizationListResponse(**data)
        assert len(response.data) == 1
        assert response.total == 1
        assert response.limit == 10
        assert response.offset == 0

    def test_pagination_validation(self, valid_org_response):
        """Test pagination field validation."""
        # Test invalid limit values
        with pytest.raises(ValidationError):
            OrganizationListResponse(
                data=[valid_org_response], total=1, limit=0, offset=0  # Below minimum
            )

        with pytest.raises(ValidationError):
            OrganizationListResponse(
                data=[valid_org_response],
                total=1,
                limit=1001,  # Above maximum
                offset=0,
            )

        # Test negative values
        with pytest.raises(ValidationError):
            OrganizationListResponse(
                data=[valid_org_response], total=-1, limit=10, offset=0
            )

        with pytest.raises(ValidationError):
            OrganizationListResponse(
                data=[valid_org_response], total=1, limit=10, offset=-1
            )

    def test_empty_list_response(self):
        """Test list response with empty data."""
        response = OrganizationListResponse(data=[], total=0, limit=10, offset=0)
        assert len(response.data) == 0
        assert response.total == 0
