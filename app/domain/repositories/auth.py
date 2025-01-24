from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models.auth import User


class UserRepository(ABC):
    """Repository interface for managing user persistence.

    This interface defines the contract for user storage operations,
    providing methods for retrieving, saving, and updating user data.
    Implementations should handle the actual storage mechanism (e.g., database).
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to look up

        Returns:
            The user if found, None otherwise

        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        """Save or update a user.

        Args:
            user: The user to save or update

        Raises:
            RepositoryError: If there's an error during save operation
        """
        pass

    @abstractmethod
    async def update_login_time(self, user_id: UUID) -> None:
        """Update the last login timestamp for a user.

        Args:
            user_id: ID of the user to update

        Raises:
            RepositoryError: If there's an error during update
            NotFoundError: If the user doesn't exist
        """
        pass
