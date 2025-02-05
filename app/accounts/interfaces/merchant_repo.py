"""Repository interface for Merchant aggregate operations.

This module defines the abstract interface for Merchant persistence operations,
extending the base repository interface with merchant-specific functionality.
"""

from abc import abstractmethod
from typing import List
from uuid import UUID

from app.accounts.entities.merchant import Merchant
from app.common.interfaces.repository_interface import RepositoryInterface


class MerchantRepository(RepositoryInterface[Merchant]):
    """Repository interface for managing merchant persistence.

    This interface defines the contract for merchant storage operations,
    extending the base repository with organization-specific queries
    and search capabilities.

    Example:
        >>> repo = MerchantRepository()
        >>> merchants = repo.list_by_organization(org_id)
        >>> for merchant in merchants:
        ...     print(merchant.name)
    """

    @abstractmethod
    def list_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[Merchant]:
        """List merchants belonging to an organization.

        Args:
            org_id: Organization's unique identifier.
            limit: Maximum number of merchants to return.
            offset: Number of merchants to skip.

        Returns:
            List of merchants for the organization.

        Raises:
            RepositoryError: If there's an error accessing the storage.
        """
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Merchant]:
        """Search merchants by name.

        Performs a case-insensitive partial match on merchant names.

        Args:
            name: Search term to match against merchant names.

        Returns:
            List of merchants matching the search term.

        Raises:
            RepositoryError: If there's an error during search.
        """
        pass
