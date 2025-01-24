from datetime import datetime
from threading import Lock
from uuid import UUID

from app.domain.models.auth import User
from app.domain.repositories.auth import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of the User repository.

    This repository stores users in memory using a dictionary with email as key.
    Intended for testing and development purposes only.

    Note:
        - Data is not persisted across application restarts
        - This implementation is not thread-safe
        - Users are indexed by email for efficient email-based lookups

    Attributes:
        users (dict): Dictionary storing users with email addresses as keys.
    """

    _instance = None
    _initialized = False

    def __init__(self):
        """Initialize the repository if not already initialized."""
        if not self._initialized:
            self._users = {}
            self._lock = Lock()
            self._initialized = True

    def __new__(cls):
        """Ensure singleton instance creation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: Email address of the user to retrieve.

        Returns:
            The user if found, None otherwise.

        Note:
            Email lookup is case-sensitive. Consider normalizing email
            addresses if case-insensitive lookup is needed.
        """
        return self._users.get(email)

    async def save(self, user: User) -> None:
        """Save or update a user in the repository.

        Args:
            user: The user entity to save.

        Note:
            If a user with the same email exists, they will be overwritten.
            This method is used for both creation and updates.
        """
        self._users[user.email] = user

    async def update_login_time(self, user_id: UUID) -> None:
        """Update the last login timestamp for a user.

        Args:
            user_id: UUID of the user to update.

        Note:
            - This operation requires iterating through all users to find
              a matching user_id since the primary index is email
            - If no user is found with the given ID, the operation is silently skipped
            - The timestamp is set to the current time when the method is called
        """
        for user in self._users.values():
            if user.user_id == user_id:
                user.last_login = datetime.now()
