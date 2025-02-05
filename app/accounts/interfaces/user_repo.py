"""Repository interface for User aggregate operations.

This module defines the abstract interface for User persistence operations,
extending the base repository interface with user-specific functionality.
"""

from abc import abstractmethod
from typing import Optional
from uuid import UUID

from app.accounts.entities.user import User
from app.common.interfaces.repository_interface import RepositoryInterface
from app.common.value_objects.email import Email


class UserRepository(RepositoryInterface[User]):
    """Repository interface for managing user persistence.

    This interface defines the contract for user storage operations,
    extending the base repository with email-based lookup and login
    tracking capabilities.

    Example:
        >>> repo = UserRepository()
        >>> user = repo.get_by_email("user@example.com")
        >>> repo.update_login_time(user.id)
    """

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        """Retrieve a user by their email address.

        Args:
            email: Email address to look up.

        Returns:
            User if found, None otherwise.

        Raises:
            RepositoryError: If there's an error during retrieval.
        """
        pass

    @abstractmethod
    def update_login_time(self, user_id: UUID) -> None:
        """Update the last login timestamp for a user.

        Args:
            user_id: ID of the user to update.

        Raises:
            RepositoryError: If there's an error during update.
            NotFoundError: If the user doesn't exist.
        """
        pass
