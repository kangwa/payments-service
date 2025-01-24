from datetime import datetime
from uuid import UUID

from app.domain.models.organization import Organization, OrganizationStatus


def test_organization_initialization():
    """Test that organization is initialized with correct default values.

    Verifies:
    - Name is set correctly
    - Status starts as PENDING
    - ID is a valid UUID
    - Timestamps are datetime objects
    - Metadata is an empty dict
    """
    org = Organization(name="Test Org")
    assert org.name == "Test Org"
    assert org.status == OrganizationStatus.PENDING
    assert isinstance(org.id, UUID)
    assert isinstance(org.created_at, datetime)
    assert isinstance(org.updated_at, datetime)
    assert org.metadata == {}


def test_organization_activation(org):
    """Test organization activation process.

    Verifies:
    - Status changes to ACTIVE
    - Updated timestamp is modified
    """
    initial_updated_at = org.updated_at

    org.activate()

    assert org.status == OrganizationStatus.ACTIVE
    assert org.updated_at > initial_updated_at


def test_organization_suspension(org):
    """Test organization suspension process.

    Verifies:
    - Status changes to SUSPENDED
    - Updated timestamp is modified
    """
    initial_updated_at = org.updated_at

    org.suspend()

    assert org.status == OrganizationStatus.SUSPENDED
    assert org.updated_at > initial_updated_at


def test_organization_metadata_update():
    """Test organization metadata handling.

    Verifies:
    - Metadata can be set during initialization
    - Metadata values are accessible
    """
    org = Organization(name="Test Org", metadata={"industry": "tech"})
    assert org.metadata["industry"] == "tech"
