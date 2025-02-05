"""In-memory repository implementation for User entities."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.accounts.entities.user import User
from app.accounts.interfaces.user_repo import UserRepository
from app.common.adapters.in_memory.repository import InMemoryRepository


class InMemoryUserRepository(InMemoryRepository[User], UserRepository):
    """In-memory implementation of UserRepository interface.
    Manages User entity persistence in memory with basic CRUD operations and
    domain-specific queries. Useful for testing scenarios.

    Inherits:
        InMemoryRepository: Base in-memory repository functionality
        UserRepository: Interface defining user-specific operations
    """

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address (case-insensitive).

        Args:
            email (str): Email address to search for

        Returns:
            Optional[User]: User with matching email or None if not found
        """
        return next(
            (
                user
                for user in self._storage.values()
                if user.email.lower() == email.lower()
            ),
            None,
        )

    def get_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[User]:
        """List users belonging to a specific organization with pagination.

        Args:
            org_id (UUID): Organization ID to filter users
            limit (int): Maximum results to return. Defaults to 100
            offset (int): Number of records to skip. Defaults to 0

        Returns:
            list[User]: Paginated list of users in the specified organization
        """
        users = [
            user for user in self._storage.values() if user.organization_id == org_id
        ]
        return users[offset : offset + limit]

    def search_by_name(self, name: str) -> list[User]:
        """Search users by name using case-insensitive partial matching.

        Args:
            name (str): Search term to match against user names

        Returns:
            list[User]: All users whose names contain the search term
        """
        return [
            user for user in self._storage.values() if name.lower() in user.name.lower()
        ]

    def update_login_time(self, user_id: UUID) -> None:
        """Update the last login timestamp for a specified user.

        Args:
            user_id (UUID): ID of the user to update

        Note:
            Silently ignores if the user doesn't exist
        """
        user = self.get(user_id)
        if user:
            user.last_login_at = datetime.now()
            self.save(user)
