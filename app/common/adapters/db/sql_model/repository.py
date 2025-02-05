from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase
from sqlmodel import Session, delete, func, select

from app.common.exceptions import RecordNotFoundError, RepositoryError, ValidationError

T = TypeVar("T")  # Domain entity type
M = TypeVar("M", bound=DeclarativeBase)  # SQLAlchemy model type


class SQLModelRepository(Generic[T, M]):
    """SQLAlchemy-based repository for managing database entities."""

    def __init__(self, session: Session, model: Type[M]):
        """Initializes the repository.

        Args:
            session (Session): The SQLAlchemy session.
            model (Type[M]): The SQLAlchemy model class.
        """
        self.session = session
        self.model = model

    def save(self, entity: T) -> T:
        """Saves an entity in the database.

        Args:
            entity (T): The entity to save.

        Returns:
            T: The saved entity.

        Raises:
            RepositoryError: If an error occurs during save.
        """
        try:
            db_model = self._to_model(entity)
            merged_model = self.session.merge(db_model)
            self.session.commit()
            self.session.refresh(merged_model)
            return self._to_entity(merged_model)
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(f"Failed to save entity {self.model.__name__}") from e

    def bulk_save(self, entities: List[T]) -> List[T]:
        """Saves multiple entities in a single transaction.

        Args:
            entities (List[T]): The list of entities to save.

        Returns:
            List[T]: The saved entities.

        Raises:
            RepositoryError: If a database error occurs.
        """
        try:
            db_models = [self._to_model(entity) for entity in entities]
            self.session.bulk_save_objects(db_models)
            self.session.commit()
            return [self._to_entity(model) for model in db_models]
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(
                f"Failed to bulk save entities of type {self.model.__name__}"
            ) from e

    def get(self, id: UUID) -> T:
        """Retrieves an entity by its ID.

        Args:
            id (UUID): The ID of the entity.

        Returns:
            T: The entity if found.

        Raises:
            RecordNotFoundError: If the entity does not exist.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = self.session.execute(stmt)
        db_model = result.scalar_one_or_none()
        if not db_model:
            raise RecordNotFoundError(entity_type=self.model.__name__, identifier=id)
        return self._to_entity(db_model)

    def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        filters: Optional[dict] = None,
    ) -> list[T]:
        """List all entities with pagination."""
        stmt = select(self.model).limit(limit).offset(offset)

        if filters:
            stmt = self._filter(stmt, filters)

        if sort_by:
            stmt = stmt.order_by(getattr(self.model, sort_by))

        results = self.session.exec(stmt).all()
        return [self._to_entity(model) for model in results]

    def find_one(self, filters: Dict[str, Any]) -> Optional[T]:
        """Finds a single entity that matches the given filters.

        Args:
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            Optional[T]: The first matching entity, or None.

        Raises:
            ValidationError: If no filters are provided.
        """
        if not filters:
            raise ValidationError("Filters are required for find_one.")

        stmt = select(self.model)
        stmt = self._filter(stmt, filters)
        result = self.session.exec(stmt)
        db_model = result.first()
        return self._to_entity(db_model) if db_model else None

    def exists(self, filters: Dict[str, Any]) -> bool:
        """Checks if any entity matches the given filters.

        Args:
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            bool: True if at least one entity matches, False otherwise.

        Raises:
            ValidationError: If no filters are provided.
        """
        if not filters:
            raise ValidationError("Filters are required for exists check.")

        stmt = select(func.count()).select_from(self.model)
        stmt = self._filter(stmt, filters)
        result = self.session.execute(stmt)
        return result.scalar_one() > 0

    def delete(self, id: UUID) -> bool:
        """Deletes an entity by its ID.

        Args:
            id (UUID): The ID of the entity.

        Returns:
            bool: True if the entity was deleted, False otherwise.

        Raises:
            RepositoryError: If a database error occurs.
        """
        try:
            stmt = delete(self.model).where(self.model.id == id)
            result = self.session.execute(stmt)
            self.session.commit()
            return result.rowcount > 0
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(
                f"Failed to delete entity {self.model.__name__} with ID {id}"
            ) from e

    def bulk_delete(self, filters: Dict[str, Any]) -> int:
        """Deletes multiple entities matching the given filters.

        Args:
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            int: The number of deleted entities.

        Raises:
            ValidationError: If no filters are provided.
            RepositoryError: If a database error occurs.
        """
        if not filters:
            raise ValidationError("Filters are required for bulk delete.")

        try:
            stmt = delete(self.model)
            stmt = self._filter(stmt, filters)
            result = self.session.execute(stmt)
            self.session.commit()
            return result.rowcount
        except Exception as e:
            self.session.rollback()
            raise RepositoryError(
                f"Failed to bulk delete entities of type {self.model.__name__}"
            ) from e

    def count(self, filters: Optional[dict] = None) -> int:
        """Count total entities."""
        stmt = select(func.count()).select_from(self.model)

        if filters:
            stmt = self._filter(stmt, filters)

        result = self.session.exec(stmt)
        return result.one()

    def _to_model(self, entity: T) -> M:
        """Converts a domain entity to an SQLAlchemy model."""
        raise NotImplementedError("Subclasses must implement `_to_model`")

    def _to_entity(self, model: M) -> T:
        """Converts an SQLAlchemy model to a domain entity."""
        raise NotImplementedError("Subclasses must implement `_to_entity`")

    def _filter(self, stmt, filters: Dict[str, Any]):
        """Applies filters to a query statement.

        Args:
            stmt: The SQLAlchemy statement to filter.
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            The modified statement with filters applied.
        """
        for field, value in filters.items():
            column = getattr(self.model, field, None)
            if not column:
                continue

            if isinstance(value, list):
                stmt = stmt.where(column.in_(value))
            elif isinstance(value, dict):
                if "min" in value:
                    stmt = stmt.where(column >= value["min"])
                if "max" in value:
                    stmt = stmt.where(column <= value["max"])
                if "like" in value:
                    stmt = stmt.where(column.like(value["like"]))
            else:
                stmt = stmt.where(column == value)

        return stmt
