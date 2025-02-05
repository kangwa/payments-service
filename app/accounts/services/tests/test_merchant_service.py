"""Test suite for MerchantService."""

from unittest.mock import Mock

import pytest

from app.accounts.entities.merchant import MerchantStatus
from app.accounts.services.merchant_service import MerchantService


class TestMerchantService:
    """Test cases for MerchantService."""

    @pytest.fixture
    def mock_repo(self):
        """Mock merchant repository fixture."""
        return Mock()

    @pytest.fixture
    def merchant_service(self, mock_repo):
        """Merchant service fixture."""
        return MerchantService(repo=mock_repo)

    def test_list_merchants_success(
        self, merchant_service, mock_repo, valid_merchant, valid_org_id
    ):
        """Test successful merchant listing."""
        # Setup
        mock_repo.list_all.return_value = [valid_merchant]
        mock_repo.count.return_value = 1

        # Execute
        merchants, total = merchant_service.list_merchants(
            org_id=valid_org_id, limit=10, offset=0
        )

        # Assert
        assert len(merchants) == 1
        assert total == 1
        assert merchants[0] == valid_merchant
        mock_repo.list_all.assert_called_once_with(
            limit=10, offset=0, filters={"organization_id": valid_org_id}
        )

    def test_list_merchants_with_status_filter(
        self, merchant_service, mock_repo, valid_merchant, valid_org_id
    ):
        """Test merchant listing with status filter."""
        # Setup
        mock_repo.list_all.return_value = [valid_merchant]
        mock_repo.count.return_value = 1

        # Execute
        merchants, total = merchant_service.list_merchants(
            org_id=valid_org_id, limit=10, offset=0, status="ACTIVE"
        )

        # Assert
        assert len(merchants) == 1
        mock_repo.list_all.assert_called_once_with(
            limit=10,
            offset=0,
            filters={"organization_id": valid_org_id, "status": MerchantStatus.ACTIVE},
        )

    def test_list_merchants_invalid_status(self, merchant_service, valid_org_id):
        """Test merchant listing with invalid status."""
        with pytest.raises(ValueError, match="Invalid status filter"):
            merchant_service.list_merchants(
                org_id=valid_org_id, limit=10, offset=0, status="INVALID"
            )

    def test_get_merchant_success(self, merchant_service, mock_repo, valid_merchant):
        """Test successful merchant retrieval."""
        # Setup
        mock_repo.get.return_value = valid_merchant

        # Execute
        merchant = merchant_service.get_merchant(valid_merchant.id)

        # Assert
        assert merchant == valid_merchant
        mock_repo.get.assert_called_once_with(valid_merchant.id)

    def test_get_merchant_not_found(
        self, merchant_service, mock_repo, valid_merchant_id
    ):
        """Test merchant retrieval when not found."""
        # Setup
        mock_repo.get.return_value = None

        # Execute and Assert
        with pytest.raises(ValueError, match="Merchant with ID .* not found"):
            merchant_service.get_merchant(valid_merchant_id)

    def test_create_merchant_success(self, merchant_service, mock_repo, valid_org_id):
        """Test successful merchant creation."""
        # Execute
        merchant = merchant_service.create_merchant(
            org_id=valid_org_id, name="Test Merchant", country_code="us", currency="usd"
        )

        # Assert
        assert merchant.name == "Test Merchant"
        assert merchant.country_code == "US"
        assert merchant.currency == "USD"
        assert merchant.organization_id == valid_org_id
        assert merchant.status == MerchantStatus.ACTIVE
        mock_repo.save.assert_called_once_with(merchant)

    def test_add_payment_method_success(
        self, merchant_service, mock_repo, valid_merchant
    ):
        """Test successful payment method addition."""
        # Setup
        mock_repo.get.return_value = valid_merchant

        # Execute
        merchant = merchant_service.add_payment_method(
            merchant_id=valid_merchant.id, payment_method="stripe"
        )

        # Assert
        assert "stripe" in merchant.payment_methods
        mock_repo.save.assert_called_once_with(merchant)

    def test_suspend_merchant_success(
        self, merchant_service, mock_repo, valid_merchant
    ):
        """Test successful merchant suspension."""
        # Setup
        mock_repo.get.return_value = valid_merchant

        # Execute
        merchant = merchant_service.suspend_merchant(valid_merchant.id)

        # Assert
        assert merchant.status == MerchantStatus.SUSPENDED
        mock_repo.save.assert_called_once_with(merchant)
