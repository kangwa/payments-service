"""Entities module for the accounts domain.

This module exports the core domain entities and their associated enums for the accounts
bounded context. These entities represent the fundamental business objects that encapsulate
critical business rules and maintain their own data consistency.

The module provides:
    - Organization and OrganizationStatus: Represents business organizations and their states
    - Merchant and MerchantStatus: Represents payment processing businesses
    - User and UserStatus: Represents authenticated system users
    - TokenData: Represents authentication token information

Typical usage example:
    from app.entities import Organization, User, Merchant, TokenData
    from app.entities import OrganizationStatus, UserStatus, MerchantStatus
    
    org = Organization(name="Acme Corp", domain="acme.com")
    user = User(email="john@acme.com", organization_id=org.id)
    merchant = Merchant(
        name="Acme Payments",
        organization_id=org.id,
        country_code="US",
        currency="USD"
    )
"""

from .merchant import Merchant, MerchantStatus
from .organization import Organization, OrganizationStatus
from .token_data import TokenData
from .user import User, UserStatus

__all__ = [
    # Entity Classes
    "Merchant",
    "Organization",
    "TokenData",
    "User",
    # Status Enums
    "MerchantStatus",
    "OrganizationStatus",
    "UserStatus",
]
