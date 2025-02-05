from datetime import datetime
from uuid import UUID, uuid4

import pytest

from app.accounts.entities.merchant import Merchant, MerchantStatus


class TestMerchant:
    """Test suite for Merchant entity."""

    @pytest.fixture
    def valid_merchant_request_data(self):
        """Fixture providing valid merchant test data."""
        return {
            "name": "Test Merchant",
            "organization_id": uuid4(),
            "country_code": "US",
            "currency": "USD",
        }

    @pytest.fixture
    def merchant(self, valid_merchant_request_data):
        """Fixture providing a valid Merchant instance."""
        return Merchant(**valid_merchant_request_data)

    def test_create_merchant_with_valid_data(self, valid_merchant_request_data):
        """Test merchant creation with valid data."""
        merchant = Merchant(**valid_merchant_request_data)

        assert isinstance(merchant.id, UUID)
        assert merchant.name == valid_merchant_request_data["name"]
        assert merchant.organization_id == valid_merchant_request_data["organization_id"]
        assert merchant.country_code == "US"
        assert merchant.currency == "USD"
        assert merchant.status == MerchantStatus.ACTIVE
        assert isinstance(merchant.created_at, datetime)
        assert isinstance(merchant.updated_at, datetime)
        assert merchant.payment_methods == []
        assert merchant.api_keys == []
        assert merchant.metadata == {}

    def test_country_code_validation(self, valid_merchant_request_data):
        """Test country code validation rules."""
        # Test invalid country codes
        with pytest.raises(
            ValueError, match="Country code must be ISO 3166-1 alpha-2 format"
        ):
            valid_merchant_request_data["country_code"] = "USA"
            Merchant(**valid_merchant_request_data)

        with pytest.raises(
            ValueError, match="Country code must be ISO 3166-1 alpha-2 format"
        ):
            valid_merchant_request_data["country_code"] = "1"
            Merchant(**valid_merchant_request_data)

        # Test valid country code gets uppercased
        valid_merchant_request_data["country_code"] = "us"
        merchant = Merchant(**valid_merchant_request_data)
        assert merchant.country_code == "US"

    def test_currency_validation(self, valid_merchant_request_data):
        """Test currency code validation rules."""
        # Test invalid currency codes
        with pytest.raises(ValueError, match="Currency must be ISO 4217 format"):
            valid_merchant_request_data["currency"] = "USDD"
            Merchant(**valid_merchant_request_data)

        with pytest.raises(ValueError, match="Currency must be ISO 4217 format"):
            valid_merchant_request_data["currency"] = "US"
            Merchant(**valid_merchant_request_data)

        # Test valid currency code gets uppercased
        valid_merchant_request_data["currency"] = "usd"
        merchant = Merchant(**valid_merchant_request_data)
        assert merchant.currency == "USD"

    def test_status_transitions(self, merchant):
        """Test merchant status transition methods."""
        assert merchant.status == MerchantStatus.ACTIVE

        merchant.suspend()
        assert merchant.status == MerchantStatus.SUSPENDED

        merchant.put_under_review()
        assert merchant.status == MerchantStatus.UNDER_REVIEW

        merchant.activate()
        assert merchant.status == MerchantStatus.ACTIVE

    def test_payment_method_management(self, merchant):
        """Test payment method addition and removal."""
        method = "stripe"

        # Test adding payment method
        merchant.add_payment_method(method)
        assert method in merchant.payment_methods

        # Test duplicate addition
        with pytest.raises(ValueError, match="Payment method stripe already exists"):
            merchant.add_payment_method(method)

        # Test removal
        merchant.remove_payment_method(method)
        assert method not in merchant.payment_methods

        # Test removing non-existent method
        with pytest.raises(ValueError, match="Payment method stripe not found"):
            merchant.remove_payment_method(method)

    def test_api_key_management(self, merchant):
        """Test API key addition and removal."""
        api_key = uuid4()

        # Test adding API key
        merchant.add_api_key(api_key)
        assert api_key in merchant.api_keys

        # Test duplicate addition
        with pytest.raises(ValueError, match=f"API key {api_key} already exists"):
            merchant.add_api_key(api_key)

        # Test removal
        merchant.remove_api_key(api_key)
        assert api_key not in merchant.api_keys

        # Test removing non-existent key
        with pytest.raises(ValueError, match=f"API key {api_key} not found"):
            merchant.remove_api_key(api_key)

    def test_is_active_property(self, merchant):
        """Test is_active property behavior."""
        assert merchant.is_active is True

        merchant.suspend()
        assert merchant.is_active is False

        merchant.put_under_review()
        assert merchant.is_active is False

        merchant.activate()
        assert merchant.is_active is True
