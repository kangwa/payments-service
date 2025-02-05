"""Test suite for organization-related value objects."""

import pytest

from app.common.value_objects.domain_name import DomainName


class TestDomainName:
    """Test cases for DomainName value object."""

    def test_valid_domain_names(self):
        """Test valid domain name formats."""
        valid_domains = [
            "example.com",
            "sub.example.com",
            "sub-domain.example.com",
            "example.co.uk",
            "123.example.com",
        ]

        for domain in valid_domains:
            domain_vo = DomainName(value=domain)
            assert str(domain_vo) == domain.lower()

    def test_domain_normalization(self):
        """Test domain name normalization."""
        domain_vo = DomainName(value="  EXAMPLE.COM  ")
        assert str(domain_vo) == "example.com"

    def test_invalid_domain_names(self):
        """Test invalid domain name formats."""
        invalid_domains = [
            "",  # Empty
            "invalid",  # No TLD
            ".com",  # No domain name
            "invalid@domain.com",  # Contains @
            "a" * 254 + ".com",  # Too long
            "domain..com",  # Consecutive dots
            "domain.c",  # TLD too short
            "-domain.com",  # Starts with hyphen
            "domain-.com",  # Ends with hyphen
        ]

        for domain in invalid_domains:
            with pytest.raises(ValueError):
                DomainName(value=domain)

    def test_domain_equality(self):
        """Test domain name equality comparison."""
        domain1 = DomainName(value="example.com")
        domain2 = DomainName(value="EXAMPLE.COM")
        domain3 = DomainName(value="other.com")

        assert domain1 == domain2
        assert domain1 != domain3
        assert domain1 != "example.com"
