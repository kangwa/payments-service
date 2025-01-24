from uuid import UUID, uuid4
from faker import Faker

import pytest

from app.domain.models.merchant import Merchant, MerchantStatus

fake = Faker()


def test_merchant_initialization(org):
    """Test that merchant is initialized with correct default values.

    Verifies:
    - Required fields are set correctly
    - Optional fields have correct default values
    - Lists are empty by default
    - Status starts as ACTIVE
    """
    merchant_name = fake.company()
    country_code = fake.country_code()
    currency_code = fake.currency_code()

    merchant = Merchant(
        organization_id=org.id,
        name=merchant_name,
        country_code=country_code,
        currency=currency_code,
    )

    assert isinstance(merchant.id, UUID)
    assert merchant.name == merchant_name
    assert merchant.country_code == country_code
    assert merchant.currency == currency_code
    assert merchant.description is None
    assert merchant.status == MerchantStatus.ACTIVE
    assert merchant.payment_methods == []
    assert merchant.api_keys == []
    assert merchant.metadata == {}


def test_status_changes(merchant):
    """Test merchant status transition methods.

    Verifies:
    - Status changes work correctly
    - Updated timestamp is modified
    - All status transitions are possible
    """
    initial_time = merchant.updated_at

    merchant.suspend()
    assert merchant.status == MerchantStatus.SUSPENDED
    assert merchant.updated_at > initial_time

    merchant.put_under_review()
    assert merchant.status == MerchantStatus.UNDER_REVIEW

    merchant.activate()
    assert merchant.status == MerchantStatus.ACTIVE


def test_payment_method_management(merchant):
    """Test payment method addition and removal.

    Verifies:
    - Methods can be added
    - Duplicate methods are rejected
    - Methods can be removed
    - Removing non-existent methods raises error
    """
    merchant.add_payment_method("card")
    assert "card" in merchant.payment_methods

    with pytest.raises(ValueError):
        merchant.add_payment_method("card")

    merchant.remove_payment_method("card")
    assert "card" not in merchant.payment_methods

    with pytest.raises(ValueError):
        merchant.remove_payment_method("card")


def test_api_key_management(merchant):
    """Test API key addition and removal.

    Verifies:
    - Keys can be added
    - Duplicate keys are rejected
    - Keys can be removed
    - Removing non-existent keys raises error
    """
    key = uuid4()
    merchant.add_api_key(key)
    assert key in merchant.api_keys

    with pytest.raises(ValueError):
        merchant.add_api_key(key)

    merchant.remove_api_key(key)
    assert key not in merchant.api_keys

    with pytest.raises(ValueError):
        merchant.remove_api_key(key)


def test_metadata_handling(org):
    """Test merchant metadata handling.

    Verifies:
    - Metadata can be set during initialization
    - Metadata values are accessible
    """
    merchant = Merchant(
        organization_id=org.id,
        name="Test Merchant",
        country_code="US",
        currency="USD",
        metadata={"business_type": "retail"},
    )
    assert merchant.metadata["business_type"] == "retail"
