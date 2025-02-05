"""Test suite for MerchantRepository interface."""

from uuid import uuid4

import pytest

from app.accounts.entities.merchant import Merchant

from .mock_repositories import MockMerchantRepository


@pytest.fixture
def merchant_repo():
    """Fixture providing a mock merchant repository."""
    return MockMerchantRepository()


@pytest.fixture
def sample_merchant():
    """Fixture providing a sample merchant entity."""
    return Merchant(
        name="Test Merchant", organization_id=uuid4(), country_code="US", currency="USD"
    )


class TestMerchantRepository:
    """Test cases for MerchantRepository interface."""

    def test_save_and_get_by_id(self, merchant_repo, sample_merchant):
        """Test saving and retrieving a merchant."""
        # Save merchant
        saved = merchant_repo.save(sample_merchant)
        assert saved.id == sample_merchant.id

        # Retrieve merchant
        retrieved = merchant_repo.get_by_id(sample_merchant.id)
        assert retrieved is not None
        assert retrieved.id == sample_merchant.id
        assert retrieved.name == sample_merchant.name

    def test_list_pagination(self, merchant_repo):
        """Test merchant listing with pagination."""
        # Create test merchants
        merchants = [
            Merchant(
                name=f"Merchant {i}",
                organization_id=uuid4(),
                country_code="US",
                currency="USD",
            )
            for i in range(5)
        ]
        for merchant in merchants:
            merchant_repo.save(merchant)

        # Test pagination
        page_1 = merchant_repo.list(limit=2, offset=0)
        assert len(page_1) == 2

        page_2 = merchant_repo.list(limit=2, offset=2)
        assert len(page_2) == 2

        page_3 = merchant_repo.list(limit=2, offset=4)
        assert len(page_3) == 1

    def test_delete(self, merchant_repo, sample_merchant):
        """Test merchant deletion."""
        # Save and then delete
        merchant_repo.save(sample_merchant)
        merchant_repo.delete(sample_merchant.id)

        # Verify deletion
        assert merchant_repo.get_by_id(sample_merchant.id) is None

        # Verify delete of non-existent merchant raises error
        with pytest.raises(ValueError):
            merchant_repo.delete(uuid4())

    def test_list_by_organization(self, merchant_repo):
        """Test listing merchants by organization."""
        org_id = uuid4()
        other_org_id = uuid4()

        # Create merchants for both organizations
        org_merchants = [
            Merchant(
                name=f"Org Merchant {i}",
                organization_id=org_id,
                country_code="US",
                currency="USD",
            )
            for i in range(3)
        ]
        other_merchants = [
            Merchant(
                name=f"Other Merchant {i}",
                organization_id=other_org_id,
                country_code="US",
                currency="USD",
            )
            for i in range(2)
        ]

        for merchant in org_merchants + other_merchants:
            merchant_repo.save(merchant)

        # Test listing by organization
        result = merchant_repo.list_by_organization(org_id)
        assert len(result) == 3
        assert all(m.organization_id == org_id for m in result)

    def test_search_by_name(self, merchant_repo):
        """Test merchant search by name."""
        # Create test merchants
        merchants = [
            Merchant(
                name="Acme Corp",
                organization_id=uuid4(),
                country_code="US",
                currency="USD",
            ),
            Merchant(
                name="Acme Subsidiaries",
                organization_id=uuid4(),
                country_code="US",
                currency="USD",
            ),
            Merchant(
                name="Other Corp",
                organization_id=uuid4(),
                country_code="US",
                currency="USD",
            ),
        ]
        for merchant in merchants:
            merchant_repo.save(merchant)

        # Test search
        results = merchant_repo.search_by_name("Acme")
        assert len(results) == 2
        assert all("Acme" in m.name for m in results)

        # Test case insensitive search
        results = merchant_repo.search_by_name("acme")
        assert len(results) == 2

        # Test no results
        results = merchant_repo.search_by_name("NonExistent")
        assert len(results) == 0
