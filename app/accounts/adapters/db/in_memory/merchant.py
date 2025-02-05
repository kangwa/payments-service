"""In-memory repository implementation for Merchant entities."""
from uuid import UUID

from app.accounts.entities.merchant import Merchant
from app.accounts.interfaces.merchant_repo import MerchantRepository
from app.common.adapters.db.in_memory.repository import InMemoryRepository


class InMemoryMerchantRepository(InMemoryRepository[Merchant], MerchantRepository):
    """In-memory implementation of MerchantRepository interface.

    Provides CRUD operations and custom queries for Merchant entities using
    an in-memory storage. Suitable for testing and development environments.

    Inherits:
        InMemoryRepository: Generic in-memory repository implementation
        MerchantRepository: Interface defining merchant-specific operations
    """

    def list_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[Merchant]:
        """Retrieve merchants belonging to a specific organization.

        Args:
            org_id (UUID): The organization ID to filter merchants
            limit (int): Maximum number of merchants to return. Defaults to 100
            offset (int): Number of merchants to skip. Defaults to 0

        Returns:
            list[Merchant]: Paginated list of merchants for the organization,
                ordered by storage insertion order
        """
        merchants = [m for m in self._storage.values() if m.organization_id == org_id]
        return merchants[offset : offset + limit]

    def search_by_name(self, name: str) -> list[Merchant]:
        """Search merchants by name using case-insensitive partial matching.

        Args:
            name (str): Search term to match against merchant names

        Returns:
            list[Merchant]: All merchants whose names contain the search term
        """
        return [m for m in self._storage.values() if name.lower() in m.name.lower()]
