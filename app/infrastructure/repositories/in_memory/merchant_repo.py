from uuid import UUID
from threading import Lock

from app.domain.models.merchant import Merchant
from app.domain.repositories.merchant import MerchantRepository


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
