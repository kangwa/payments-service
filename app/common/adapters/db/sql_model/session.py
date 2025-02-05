"""
Session management and database initialization for SQLModel implementations

Provides:
- Session factory with context management
- Database schema initialization
- Thread-safe session handling
"""

from sqlmodel import Session, SQLModel

from .config import engine


def get_session() -> Session:
    """Context manager for database sessions with automatic cleanup.

    Usage:
        with get_session() as session:
            session.add(...)
            session.commit()

    Yields:
        Session: Database session bound to the engine's connection pool
    """
    with Session(engine) as session:
        return session


def create_db_and_tables():
    """Initialize database schema by creating all registered SQLModel tables.

    Warning:
        - Only for development/testing environments
        - Always use migrations (Alembic) for production systems
    """
    SQLModel.metadata.create_all(engine)
