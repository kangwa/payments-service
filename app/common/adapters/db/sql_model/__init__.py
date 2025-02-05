"""SQLModel-based database adapters for SQLAlchemy storage.

This package provides SQLModel implementations of repository interfaces,
designed for production use with SQL databases. These implementations use
SQLModel (built on SQLAlchemy) for database operations and provide type-safe
data access.

Example:
    >>> from app.common.adapters.sql_model import SQLModelRepository
    >>> repo = SQLModelRepository[User](session=session)
    >>> user = repo.save(user)
    >>> retrieved = repo.get(user.id)

Note:
    SQLModel adapters require:
    - Database configuration in settings
    - SQLAlchemy session management
    - Database migration setup
    - Proper model definitions
"""

from .config import get_engine
from .repository import SQLModelRepository
from .session import create_db_and_tables, get_session

__all__ = ["get_engine", "get_session", "create_db_and_tables", "SQLModelRepository"]
