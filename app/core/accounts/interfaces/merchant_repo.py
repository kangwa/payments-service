from abc import ABC, abstractmethod
from uuid import UUID

from app.core.accounts.models import Merchant


class MerchantRepository(ABC):
    """Repository interface for managing merchant persistence.

    This interface defines the contract for merchant storage operations,
    providing methods for creating, retrieving, and listing merchants.
    Implementations should handle the actual storage mechanism (e.g., database).
    """

    @abstractmethod
    async def save(self, merchant: Merchant) -> None:
        """Save or update a merchant.

        Args:
            merchant: The merchant to save or update

        Raises:
            RepositoryError: If there's an error during save operation
        """
        pass

    @abstractmethod
    async def get(self, merchant_id: UUID) -> Merchant | None:
        """Retrieve a merchant by their ID.

        Args:
            merchant_id: The unique identifier of the merchant

        Returns:
            The merchant if found, None otherwise

        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass

    @abstractmethod
    async def list_by_organization(self, org_id: UUID) -> list[Merchant]:
        """List all merchants belonging to an organization.

        Args:
            org_id: The ID of the organization to list merchants for

        Returns:
            List of merchants belonging to the organization.
            Returns empty list if no merchants are found.

        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass
