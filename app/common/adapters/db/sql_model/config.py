"""
Database engine configuration and management for SQLModel

Handles:
- Engine creation with connection pooling
- Database URL resolution from settings
- DBMS-specific connection arguments
"""

from sqlmodel import create_engine

from app.settings import settings


def get_engine():
    """Create and configure the SQLModel database engine with connection pooling.

    Returns:
        Engine: Configured SQLAlchemy engine instance

    Raises:
        RuntimeError: If database configuration is invalid
    """
    # SQLite-specific connection parameters
    connect_args = {}
    if "sqlite" in settings.db_url:
        connect_args["check_same_thread"] = False

    try:
        return create_engine(
            settings.db_url,
            connect_args=connect_args,
            # pool_size=settings.db_pool_size,
            # max_overflow=settings.db_max_overflow,
            # pool_recycle=settings.db_pool_recycle,
            # echo=settings.db_echo,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize database engine: {str(e)}") from e


# Shared engine instance
engine = get_engine()
