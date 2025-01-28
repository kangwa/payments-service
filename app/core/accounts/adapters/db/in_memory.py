from typing import List, Tuple
from uuid import UUID
from threading import Lock

from app.core.accounts.interfaces.merchant_repo import MerchantRepository
from app.core.accounts.interfaces.organization_repo import OrganizationRepository
from app.core.accounts.models.merchant_models import Merchant
from app.core.accounts.models.organization_models import Organization


class InMemoryMerchantRepository(MerchantRepository):
    """Thread-safe in-memory implementation for Merchant persistence.

    This repository stores merchants in memory using a dictionary with UUID keys.
    All operations are protected by a threading.Lock to ensure thread safety.

    Note:
        This implementation is primarily intended for testing and development.
        Data is not persisted across application restarts.
    """

    def __init__(self):
        """Initialize an empty merchant repository with thread lock."""
        self._data = {}
        self._lock = Lock()

    async def save(self, merchant: Merchant) -> None:
        """Save or update a merchant in the repository.

        Args:
            merchant: The merchant entity to save.

        Note:
            If a merchant with the same ID exists, it will be overwritten.
        """
        with self._lock:
            self._data[merchant.id] = merchant

    async def get(self, merchant_id: UUID) -> Merchant | None:
        """Retrieve a merchant by ID.

        Args:
            merchant_id: UUID of the merchant to retrieve.

        Returns:
            The merchant if found, None otherwise.
        """
        return self._data.get(merchant_id)

    async def list_by_organization(self, org_id: UUID) -> list[Merchant]:
        """List all merchants belonging to an organization.

        Args:
            org_id: UUID of the organization.

        Returns:
            List of merchants associated with the organization,
            may be empty if no merchants are found.
        """
        return [m for m in self._data.values() if m.organization_id == org_id]

    async def update(self, merchant: Merchant) -> None:
        """Update an existing merchant.

        Args:
            merchant: The merchant entity with updated data.

        Note:
            Operation is skipped if merchant ID does not exist in repository.
        """
        with self._lock:
            if merchant.id in self._data:
                self._data[merchant.id] = merchant

    async def delete(self, merchant_id: UUID) -> bool:
        """Delete a merchant from the repository.

        Args:
            merchant_id: UUID of the merchant to delete.

        Returns:
            True if merchant was found and deleted, False if merchant was not found.
        """
        with self._lock:
            return self._data.pop(merchant_id, None) is not None

    async def list_all(self) -> list[Merchant]:
        """Retrieve all merchants in the repository.

        Returns:
            List of all merchants, may be empty if repository is empty.
        """
        return list(self._data.values())


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
