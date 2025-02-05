"""Test suite for merchant schemas."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from app.accounts.schemas.merchant_schemas import (
    MerchantCreateRequest,
    MerchantListResponse,
    MerchantResponse,
)


class TestMerchantCreateRequest:
    """Test cases for MerchantCreateRequest schema."""

    def test_valid_create_request(self, valid_merchant_request_data):
        """Test creating request with valid data."""
        request = MerchantCreateRequest(**valid_merchant_request_data)
        assert request.name == valid_merchant_request_data["name"]
        assert request.country_code == valid_merchant_request_data["country_code"]
        assert request.currency == valid_merchant_request_data["currency"]
        assert request.status == valid_merchant_request_data["status"]
        assert str(request.organization_id) == valid_merchant_request_data["organization_id"]

    def test_name_validation(self, valid_merchant_request_data):
        """Test name field validation rules."""
        # Test empty name
        data = valid_merchant_request_data.copy()
        data["name"] = ""
        with pytest.raises(ValidationError) as exc:
            MerchantCreateRequest(**data)
        assert "name" in str(exc.value)

        # Test too long name
        data["name"] = "A" * 101
        with pytest.raises(ValidationError) as exc:
            MerchantCreateRequest(**data)
        assert "name" in str(exc.value)

    def test_country_code_validation(self, valid_merchant_request_data):
        """Test country code validation rules."""
        invalid_codes = [
            "",  # Empty
            "U",  # Too short
            "USA",  # Too long
            "12",  # Numbers
            "us",  # Lowercase
        ]

        data = valid_merchant_request_data.copy()
        for code in invalid_codes:
            data["country_code"] = code
            with pytest.raises(ValidationError) as exc:
                MerchantCreateRequest(**data)
            assert "country_code" in str(exc.value)

    def test_currency_validation(self, valid_merchant_request_data):
        """Test currency code validation rules."""
        invalid_currencies = [
            "",  # Empty
            "US",  # Too short
            "USDD",  # Too long
            "123",  # Numbers
            "usd",  # Lowercase
        ]

        data = valid_merchant_request_data.copy()
        for currency in invalid_currencies:
            data["currency"] = currency
            with pytest.raises(ValidationError) as exc:
                MerchantCreateRequest(**data)
            assert "currency" in str(exc.value)

    def test_status_validation(self, valid_merchant_request_data):
        """Test status field validation."""
        data = valid_merchant_request_data.copy()
        data["status"] = "INVALID_STATUS"
        with pytest.raises(ValidationError) as exc:
            MerchantCreateRequest(**data)
        assert "status" in str(exc.value)

    def test_organization_id_validation(self, valid_merchant_request_data):
        """Test organization_id field validation."""
        data = valid_merchant_request_data.copy()
        data["organization_id"] = "invalid-uuid"
        with pytest.raises(ValidationError) as exc:
            MerchantCreateRequest(**data)
        assert "organization_id" in str(exc.value)


class TestMerchantResponse:
    """Test cases for MerchantResponse schema."""

    def test_valid_response(self, valid_merchant_response_data):
        """Test creating response with valid data."""
        response = MerchantResponse(**valid_merchant_response_data)
        assert isinstance(response.id, UUID)
        assert response.name == valid_merchant_response_data["name"]
        assert response.country_code == valid_merchant_response_data["country_code"]
        assert response.currency == valid_merchant_response_data["currency"]
        assert response.status == valid_merchant_response_data["status"]

    def test_json_serialization(self, valid_merchant_response_data):
        """Test JSON serialization of merchant response."""
        response = MerchantResponse(**valid_merchant_response_data)
        json_data = response.model_dump_json()
        assert all(
            field in json_data
            for field in ["id", "name", "country_code", "currency", "status"]
        )


class TestMerchantListResponse:
    """Test cases for MerchantListResponse schema."""

    @pytest.fixture
    def valid_merchant_response(self, valid_merchant_response_data):
        """Fixture providing valid merchant response."""
        return MerchantResponse(**valid_merchant_response_data)

    def test_valid_list_response(self, valid_merchant_response):
        """Test creating list response with valid data."""
        data = {"data": [valid_merchant_response], "total": 1, "limit": 10, "offset": 0}
        response = MerchantListResponse(**data)
        assert len(response.data) == 1
        assert response.total == 1
        assert response.limit == 10
        assert response.offset == 0

    def test_pagination_validation(self, valid_merchant_response):
        """Test pagination field validation."""
        # Test invalid limit values
        with pytest.raises(ValidationError):
            MerchantListResponse(
                data=[valid_merchant_response],
                total=1,
                limit=0,  # Below minimum
                offset=0,
            )

        with pytest.raises(ValidationError):
            MerchantListResponse(
                data=[valid_merchant_response],
                total=1,
                limit=1001,  # Above maximum
                offset=0,
            )

        # Test negative values
        with pytest.raises(ValidationError):
            MerchantListResponse(
                data=[valid_merchant_response], total=-1, limit=10, offset=0
            )

        with pytest.raises(ValidationError):
            MerchantListResponse(
                data=[valid_merchant_response], total=1, limit=10, offset=-1
            )

    def test_empty_list_response(self):
        """Test list response with empty data."""
        response = MerchantListResponse(data=[], total=0, limit=10, offset=0)
        assert len(response.data) == 0
        assert response.total == 0
