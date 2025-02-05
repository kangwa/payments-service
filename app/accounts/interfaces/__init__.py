"""Repository interfaces for the accounts domain.

This module exports the repository interfaces that define the persistence
contracts for the accounts domain. These interfaces follow the repository
pattern from Domain-Driven Design and provide the abstractions needed to
separate domain logic from storage concerns.

The module provides:
    - MerchantRepository: Interface for merchant aggregate persistence
    - OrganizationRepository: Interface for organization aggregate persistence
    - UserRepository: Interface for user aggregate persistence

Each repository interface extends the base RepositoryInterface with
domain-specific query and persistence operations.

Example:
    >>> from app.accounts.interfaces import UserRepository, OrganizationRepository
    >>> from app.accounts.adapters.db.sql_model.user import SQLUserRepository
    >>>
    >>> user_repo: UserRepository = SQLUserRepository()
    >>> org_repo: OrganizationRepository = SQLOrganizationRepository()
"""

from .merchant_repo import MerchantRepository
from .organization_repo import OrganizationRepository
from .user_repo import UserRepository

__all__ = [
    "MerchantRepository",
    "OrganizationRepository",
    "UserRepository",
]
