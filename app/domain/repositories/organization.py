from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.organization import Organization


class OrganizationRepository(ABC):
    """Repository interface for managing organization persistence.

    This interface defines the contract for organization storage operations,
    providing methods for creating, retrieving, listing, and counting organizations.
    Implementations should handle the actual storage mechanism (e.g., database).
    """

    @abstractmethod
    async def save(self, organization: Organization) -> None:
        """Save or update an organization.

        Args:
            organization: The organization to save or update

        Raises:
            RepositoryError: If there's an error during save operation
        """
        pass

    @abstractmethod
    async def get(self, org_id: UUID) -> Organization | None:
        """Retrieve an organization by its ID.

        Args:
            org_id: The unique identifier of the organization

        Returns:
            The organization if found, None otherwise

        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass

    @abstractmethod
    async def list(self) -> list[Organization]:
        """List all organizations.

        Returns:
            List of all organizations.
            Returns empty list if no organizations exist.

        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """Get the total number of organizations.

        Returns:
            The total count of organizations

        Raises:
            RepositoryError: If there's an error during counting
        """
        pass
