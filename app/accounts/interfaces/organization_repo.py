"""Repository interface for Organization aggregate operations.

This module defines the abstract interface for Organization persistence
operations, extending the base repository interface with organization-specific
functionality.
"""

from app.accounts.entities.organization import Organization
from app.common.interfaces.repository_interface import RepositoryInterface


class OrganizationRepository(RepositoryInterface[Organization]):
    """Repository interface for managing organization persistence.

    This interface defines the contract for organization storage operations,
    providing methods for creating, retrieving, listing, and counting
    organizations.

    Example:
        >>> repo = OrganizationRepository()
        >>> org = repo.get_by_id(org_id)
        >>> org.activate()
        >>> repo.save(org)
    """
