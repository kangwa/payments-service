"""Value objects for the accounts domain.

This package provides value objects that encapsulate domain validation rules
and business invariants. Value objects are immutable and are considered equal
based on their attributes rather than identity.

Subpackages:
    auth: Authentication-related value objects (Email, Password)
    domain: Domain name validation (DomainName)
    organization: Organization data validation (OrganizationName)
"""

from app.common.value_objects.domain_name import DomainName
from app.common.value_objects.email import Email

__all__ = ["Email", "DomainName"]
