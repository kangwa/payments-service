"""Test suite for organization-related value objects."""

import pytest

from app.accounts.value_objects.organization_name import OrganizationName


class TestOrganizationName:
    """Test cases for OrganizationName value object."""

    def test_valid_organization_names(self):
        """Test valid organization name formats."""
        valid_names = [
            "Acme Corporation",
            "123 Industries",
            "Company & Co.",
            "First Second Third",
            "A" * OrganizationName.MAX_LENGTH,
        ]

        for name in valid_names:
            name_vo = OrganizationName(value=name)
            assert str(name_vo) == name

    def test_name_normalization(self):
        """Test organization name normalization."""
        name_vo = OrganizationName(value="  Acme Corporation  ")
        assert str(name_vo) == "Acme Corporation"

    def test_invalid_organization_names(self):
        """Test invalid organization name formats."""
        invalid_names = [
            "",  # Empty
            "A",  # Too short
            "A" * (OrganizationName.MAX_LENGTH + 1),  # Too long
            "   ",  # Only whitespace
            "###",  # Only special characters
        ]

        for name in invalid_names:
            with pytest.raises(ValueError):
                OrganizationName(value=name)

    def test_name_equality(self):
        """Test organization name equality comparison."""
        name1 = OrganizationName(value="Acme Corp")
        name2 = OrganizationName(value="Acme Corp")
        name3 = OrganizationName(value="Other Corp")

        assert name1 == name2
        assert name1 != name3
        assert name1 != "Acme Corp"
