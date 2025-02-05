"""Test suite for the merchant API endpoints."""

from uuid import UUID

from app.common.exceptions import ValidationError


class TestMerchantAPI:
    """Test cases for merchant endpoints."""

    def test_create_merchant_success(
        self, client, mock_merchant_service, valid_merchant_request_data, valid_merchant, valid_merchant_response_data
    ):
        """Test successful merchant creation."""
        # Setup
        mock_merchant_service.create_merchant.return_value = valid_merchant_response_data

        # Execute
        response = client.post(
            f"/accounts/organizations/{valid_merchant_request_data['organization_id']}/merchants",
            json=valid_merchant_request_data,
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == valid_merchant.name
        assert data["country_code"] == valid_merchant.country_code

        # Verify service call
        mock_merchant_service.create_merchant.assert_called_once_with(
            org_id=UUID(valid_merchant_request_data["organization_id"]),
            name=valid_merchant_request_data["name"],
            country_code=valid_merchant_request_data["country_code"],
            currency=valid_merchant_request_data["currency"],
        )

    def test_list_merchants_success(
        self, client, mock_merchant_service, valid_merchant, valid_org_id
    ):
        """Test successful merchant listing."""
        # Setup
        mock_merchant_service.list_merchants.return_value = ([valid_merchant], 1)

        # Execute
        response = client.get(f"/accounts/organizations/{valid_org_id}/merchants")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == valid_merchant.name

        # Verify service call
        mock_merchant_service.list_merchants.assert_called_once_with(
            limit=100, offset=0, status=None, org_id=valid_org_id
        )

    def test_list_merchants_with_filters(
        self, client, mock_merchant_service, valid_org_id
    ):
        """Test merchant listing with filters."""
        # Setup
        mock_merchant_service.list_merchants.return_value = ([], 0)

        # Execute
        response = client.get(
            f"/accounts/organizations/{valid_org_id}/merchants?status=ACTIVE&limit=10&offset=0"
        )

        # Assert
        assert response.status_code == 200
        mock_merchant_service.list_merchants.assert_called_once_with(
            limit=10, offset=0, status="ACTIVE", org_id=valid_org_id
        )

    def test_create_merchant_validation_error(
        self, client, mock_merchant_service, valid_merchant_request_data
    ):
        """Test merchant creation with validation error."""
        # Setup
        mock_merchant_service.create_merchant.side_effect = ValidationError(
            "Invalid country code"
        )

        # Execute
        response = client.post(
            f"/accounts/organizations/{valid_merchant_request_data['organization_id']}/merchants",
            json=valid_merchant_request_data,
        )

        # Assert
        assert response.status_code == 422
        assert "Invalid country code" in response.json()["detail"]
