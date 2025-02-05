from datetime import datetime
from uuid import UUID

import pytest

from app.accounts.entities.organization import Organization, OrganizationStatus


class TestOrganization:
    """Test suite for Organization entity."""

    def test_create_organization_with_valid_data(self, valid_org_data):
        """Test organization creation with valid data."""
        org = Organization(**valid_org_data)

        assert isinstance(org.id, UUID)
        assert org.name == valid_org_data["name"]
        assert org.domain == valid_org_data["domain"]
        assert org.status == valid_org_data["status"]
        assert isinstance(org.created_at, datetime)
        assert isinstance(org.updated_at, datetime)
        assert org.metadata == {}

    def test_domain_validation(self, valid_org_data):
        """Test domain validation rules."""
        # Test invalid domains
        with pytest.raises(ValueError, match="Invalid domain format"):
            valid_org_data["domain"] = "invalid"
            Organization(**valid_org_data)

        with pytest.raises(ValueError, match="Invalid domain format"):
            valid_org_data["domain"] = ""
            Organization(**valid_org_data)

        # Test domain gets lowercased
        valid_org_data["domain"] = "TEST.COM"
        org = Organization(**valid_org_data)
        assert org.domain == "test.com"

    def test_status_transitions(self, valid_organization):
        """Test organization status transition methods."""
        valid_organization.activate()
        assert valid_organization.status == OrganizationStatus.ACTIVE

        valid_organization.suspend()
        assert valid_organization.status == OrganizationStatus.SUSPENDED

    def test_is_active_property(self, valid_organization):
        """Test is_active property behavior."""
        valid_organization.status = OrganizationStatus.PENDING
        assert valid_organization.is_active is False

        valid_organization.activate()
        assert valid_organization.is_active is True

        valid_organization.suspend()
        assert valid_organization.is_active is False
