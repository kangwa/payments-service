from threading import Lock
from typing import List, Tuple
from uuid import UUID

from app.domain.models.organization import Organization
from app.domain.repositories.organization import OrganizationRepository


class InMemoryOrganizationRepository(OrganizationRepository):
    """Thread-safe singleton in-memory implementation for Organization persistence.

    This repository implements a singleton pattern for organization storage,
    ensuring only one instance exists across the application. All operations
    are protected by a threading.Lock to ensure thread safety.

    Note:
        - This implementation is primarily intended for testing and development
        - Data is not persisted across application restarts
        - Uses singleton pattern to maintain single source of truth

    Attributes:
        _instance: Class variable holding the singleton instance
        _initialized: Flag to ensure single initialization of instance attributes
        _data: Dictionary storing organizations with UUID keys
        _lock: Threading lock for thread-safe operations
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Ensure singleton instance creation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the repository if not already initialized."""
        if not self._initialized:
            self._data = {}
            self._lock = Lock()
            self._initialized = True

    async def save(self, organization: Organization) -> None:
        """Save or update an organization in the repository.

        Args:
            organization: The organization entity to save.

        Note:
            If an organization with the same ID exists, it will be overwritten.
        """
        with self._lock:
            print(organization.id)
            self._data[organization.id] = organization

    async def get(self, org_id: UUID) -> Organization | None:
        """Retrieve an organization by ID.

        Args:
            org_id: UUID of the organization to retrieve.

        Returns:
            The organization if found, None otherwise.
        """
        return self._data.get(org_id)

    async def list(
        self, limit: int, offset: int, filters: dict = None
    ) -> Tuple[List[Organization], int]:
        """Retrieve a paginated list of organizations with optional filtering.

        Args:
            limit: Maximum number of organizations to return.
            offset: Number of organizations to skip.
            filters: Optional dictionary of attribute-value pairs to filter by.

        Returns:
            List of organizations matching the criteria within the pagination bounds.

        Note:
            Filtering is done via exact matching on organization attributes.
        """
        with self._lock:
            filtered = self._apply_filters(filters)
            return filtered[offset : offset + limit]

    async def count(self, filters: dict = None) -> int:
        """Count organizations matching the optional filters.

        Args:
            filters: Optional dictionary of attribute-value pairs to filter by.

        Returns:
            Total count of organizations matching the filters.
        """
        with self._lock:
            return len(self._apply_filters(filters))

    def _apply_filters(self, filters: dict = None) -> List[Organization]:
        """Internal method to filter organizations by attributes.

        Args:
            filters: Dictionary of attribute-value pairs to filter by.

        Returns:
            List of organizations matching all filter criteria.
        """
        if not filters:
            return list(self._data.values())

        return [
            org
            for org in self._data.values()
            if all(getattr(org, key) == value for key, value in filters.items())
        ]

    async def delete(self, org_id: UUID) -> bool:
        """Delete an organization from the repository.

        Args:
            org_id: UUID of the organization to delete.

        Returns:
            True if organization was found and deleted, False if not found.
        """
        with self._lock:
            return self._data.pop(org_id, None) is not None

    async def clear(self):
        """Remove all organizations from the repository.

        Note:
            This is primarily useful for testing scenarios.
        """
        with self._lock:
            self._data.clear()
