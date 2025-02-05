"""Test suite for OrganizationRepository interface."""

from uuid import uuid4

import pytest

from app.accounts.entities.organization import Organization, OrganizationStatus

from .mock_repositories import MockOrganizationRepository


@pytest.fixture
def org_repo():
    """Fixture providing a mock organization repository."""
    return MockOrganizationRepository()


@pytest.fixture
def sample_organization():
    """Fixture providing a sample organization entity."""
    return Organization(name="Test Organization", domain="test.com")


class TestOrganizationRepository:
    """Test cases for OrganizationRepository interface."""

    def test_save_and_get_by_id(self, org_repo, sample_organization):
        """Test saving and retrieving an organization."""
        # Save organization
        saved = org_repo.save(sample_organization)
        assert saved.id == sample_organization.id

        # Retrieve organization
        retrieved = org_repo.get_by_id(sample_organization.id)
        assert retrieved is not None
        assert retrieved.id == sample_organization.id
        assert retrieved.name == sample_organization.name
        assert retrieved.domain == sample_organization.domain

    def test_list_pagination(self, org_repo):
        """Test organization listing with pagination."""
        # Create test organizations
        organizations = [
            Organization(name=f"Organization {i}", domain=f"org{i}.com")
            for i in range(5)
        ]
        for org in organizations:
            org_repo.save(org)

        # Test pagination
        page_1 = org_repo.list(limit=2, offset=0)
        assert len(page_1) == 2

        page_2 = org_repo.list(limit=2, offset=2)
        assert len(page_2) == 2

        page_3 = org_repo.list(limit=2, offset=4)
        assert len(page_3) == 1

    def test_delete(self, org_repo, sample_organization):
        """Test organization deletion."""
        # Save and then delete
        org_repo.save(sample_organization)
        org_repo.delete(sample_organization.id)

        # Verify deletion
        assert org_repo.get_by_id(sample_organization.id) is None

        # Verify delete of non-existent organization raises error
        with pytest.raises(ValueError):
            org_repo.delete(uuid4())

    def test_count(self, org_repo):
        """Test organization counting."""
        assert org_repo.count() == 0

        # Add organizations
        organizations = [
            Organization(name=f"Org {i}", domain=f"org{i}.com") for i in range(3)
        ]
        for org in organizations:
            org_repo.save(org)

        assert org_repo.count() == 3

    def test_status_persistence(self, org_repo, sample_organization):
        """Test persistence of organization status changes."""
        # Save initial state
        org_repo.save(sample_organization)
        assert sample_organization.status == OrganizationStatus.PENDING

        # Modify and save
        retrieved = org_repo.get_by_id(sample_organization.id)
        retrieved.activate()
        org_repo.save(retrieved)

        # Verify status change persisted
        updated = org_repo.get_by_id(sample_organization.id)
        assert updated.status == OrganizationStatus.ACTIVE
