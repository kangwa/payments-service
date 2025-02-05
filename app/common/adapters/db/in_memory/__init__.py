"""In-memory storage adapters for testing and development.

This package provides in-memory implementations of repository interfaces,
primarily used for testing and development purposes. These implementations
store data in memory using Python data structures and provide the same
interface as their persistent counterparts.

Example:
    >>> from app.common.adapters.in_memory import InMemoryRepository
    >>> repo = InMemoryRepository[User]()
    >>> user = repo.save(user)
    >>> retrieved = repo.get(user.id)

Note:
    In-memory adapters are not suitable for production use as data is lost
    when the application restarts. They are intended for:
    - Unit testing
    - Development/debugging
    - Prototyping
    - CI/CD environments
"""

from app.common.adapters.db.in_memory.repository import InMemoryRepository

__all__ = ["InMemoryRepository"]
