"""
SQL model adapter for the common module.

This module contains the SQLAlchemy models and related database
operations for the common module. It provides the necessary structure
and behavior to interact with a SQL-based database system, such as
SQLite or PostgreSQL, for persisting domain entities.

The models define the structure of the database tables and the
relationships between them. The module also includes session management
and other database-related utilities necessary for CRUD operations.

Modules:
    - config: Contains database configuration settings.
    - repository: Provides the SQLAlchemy repository implementation
      for interacting with the database.
    - session: Handles SQLAlchemy session management for database
      interactions.

"""
