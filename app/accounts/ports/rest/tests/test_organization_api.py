"""Test suite for organization API endpoints."""

from uuid import UUID

from app.common.exceptions import ValidationError


class TestOrganizationAPI:
    """Test cases for organization endpoints."""

    def test_create_organization_success(
        self, client, mock_organization_service, valid_org_data, valid_organization
    ):
        """Test successful organization creation."""
        # Setup
        mock_organization_service.create_organization.return_value = valid_organization

        # Execute
        response = client.post("/accounts/organizations", json=valid_org_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == valid_organization.name
        assert data["domain"] == valid_organization.domain

        # Verify service call
        mock_organization_service.create_organization.assert_called_once_with(
            name=valid_org_data["name"], domain=valid_org_data["domain"]
        )

    def test_create_organization_validation_error(
        self, client, mock_organization_service, valid_org_data
    ):
        """Test organization creation with validation error."""
        # Setup
        mock_organization_service.create_organization.side_effect = ValidationError(
            "Invalid domain format"
        )

        # Execute
        response = client.post("/accounts/organizations", json=valid_org_data)

        # Assert
        assert response.status_code == 422
        assert "Invalid domain format" in response.json()["detail"]

    def test_list_organizations_success(
        self, client, mock_organization_service, valid_organization
    ):
        """Test successful organization listing."""
        # Setup
        mock_organization_service.list_organizations.return_value = (
            [valid_organization],
            1,
        )

        # Execute
        response = client.get("/accounts/organizations")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == valid_organization.name

    def test_list_organizations_with_filters(self, client, mock_organization_service):
        """Test organization listing with filters."""
        # Setup
        mock_organization_service.list_organizations.return_value = ([], 0)

        # Execute
        response = client.get("/accounts/organizations?status=ACTIVE&limit=10&offset=0")

        # Assert
        assert response.status_code == 200
        mock_organization_service.list_organizations.assert_called_once_with(
            limit=10, offset=0, status="ACTIVE"
        )

    def test_suspend_organization_success(
        self, client, mock_organization_service, valid_organization
    ):
        """Test successful organization suspension."""
        # Setup
        mock_organization_service.suspend_organization.return_value = valid_organization

        # Execute
        response = client.post(
            f"/accounts/organizations/{valid_organization.id}/suspend"
        )

        # Assert
        assert response.status_code == 200
        mock_organization_service.suspend_organization.assert_called_once_with(
            valid_organization.id
        )
