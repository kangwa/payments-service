"""In-memory repository implementation for Organization entities."""
from typing import Optional

from app.accounts.entities.organization import Organization
from app.accounts.interfaces.organization_repo import OrganizationRepository
from app.common.adapters.in_memory.repository import InMemoryRepository


class InMemoryOrganizationRepository(
    InMemoryRepository[Organization], OrganizationRepository
):
    """In-memory implementation of OrganizationRepository interface.
    Provides persistence operations and custom queries for Organization entities
    using an in-memory store. Primarily used for testing and temporary storage.

    Inherits:
        InMemoryRepository: Generic base repository implementation
        OrganizationRepository: Interface defining organization-specific operations
    """

    def get_by_domain(self, domain: str) -> Optional[Organization]:
        """Find an organization by its domain using case-insensitive matching.

        Args:
            domain (str): Domain to search for (e.g., "example.com")

        Returns:
            Optional[Organization]: Matching organization or None if not found
        """
        return next(
            (
                org
                for org in self._storage.values()
                if org.domain.lower() == domain.lower()
            ),
            None,
        )

    def get_by_name(self, name: str) -> Optional[Organization]:
        """Find an organization by exact name match (case-insensitive).

        Args:
            name (str): Exact organization name to search for

        Returns:
            Optional[Organization]: Matching organization or None if not found
        """
        return next(
            (org for org in self._storage.values() if org.name.lower() == name.lower()),
            None,
        )

    def list_by_type(
        self, org_type: str, limit: int = 100, offset: int = 0
    ) -> list[Organization]:
        """List organizations filtered by type with pagination support.

        Args:
            org_type (str): Organization type to filter by
            limit (int): Maximum results to return. Defaults to 100
            offset (int): Number of records to skip. Defaults to 0

        Returns:
            list[Organization]: Paginated list of organizations of specified type
        """
        orgs = [org for org in self._storage.values() if org.type == org_type]
        return orgs[offset : offset + limit]

    def search(
        self, query: str, limit: int = 100, offset: int = 0
    ) -> list[Organization]:
        """Search organizations by name or domain using case-insensitive matching.

        Args:
            query (str): Search term to match against name or domain
            limit (int): Maximum results to return. Defaults to 100
            offset (int): Number of records to skip. Defaults to 0

        Returns:
            list[Organization]: Paginated list of matching organizations
        """
        query = query.lower()
        orgs = [
            org
            for org in self._storage.values()
            if query in org.name.lower() or query in org.domain.lower()
        ]
        return orgs[offset : offset + limit]
