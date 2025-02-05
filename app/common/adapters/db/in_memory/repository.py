from typing import Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from app.common.exceptions import RecordNotFoundError, RepositoryError, ValidationError

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """In-memory implementation of the RepositoryInterface.

    Stores entities in a dictionary for quick lookups.
    """

    def __init__(self):
        """Initializes an empty in-memory repository."""
        self._storage: Dict[UUID, T] = {}

    def save(self, entity: T) -> T:
        """Saves an entity in the repository.

        Args:
            entity (T): The entity to be saved.

        Returns:
            T: The saved entity.

        Raises:
            RepositoryError: If an unexpected error occurs.
        """
        try:
            self._storage[self._get_id(entity)] = entity
            return entity
        except Exception as e:
            raise RepositoryError(
                f"Failed to save entity {self._get_entity_name()}"
            ) from e

    def bulk_save(self, entities: List[T]) -> List[T]:
        """Saves multiple entities in the repository.

        Args:
            entities (List[T]): The list of entities to save.

        Returns:
            List[T]: The saved entities.

        Raises:
            RepositoryError: If an unexpected error occurs.
        """
        try:
            for entity in entities:
                self._storage[self._get_id(entity)] = entity
            return entities
        except Exception as e:
            raise RepositoryError(
                f"Failed to bulk save entities of type {self._get_entity_name()}"
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
        entity = self._storage.get(id)
        if not entity:
            raise RecordNotFoundError(
                entity_type=self._get_entity_name(), identifier=id
            )
        return entity

    def find_one(self, filters: Dict[str, any]) -> Optional[T]:
        """Finds a single entity matching the provided filters.

        Args:
            filters (Dict[str, any]): Filtering conditions.

        Returns:
            Optional[T]: The matched entity, or None.

        Raises:
            ValidationError: If no filters are provided.
        """
        if not filters:
            raise ValidationError("Filters are required for find_one.")

        for entity in self._storage.values():
            if all(getattr(entity, key) == value for key, value in filters.items()):
                return entity
        return None

    def exists(self, filters: Dict[str, any]) -> bool:
        """Checks if any entity matches the given filters.

        Args:
            filters (Dict[str, any]): Filtering conditions.

        Returns:
            bool: True if at least one entity matches, False otherwise.

        Raises:
            ValidationError: If no filters are provided.
        """
        if not filters:
            raise ValidationError("Filters are required for exists check.")

        return any(
            all(getattr(entity, key) == value for key, value in filters.items())
            for entity in self._storage.values()
        )

    def delete(self, id: UUID) -> bool:
        """Deletes an entity by its ID.

        Args:
            id (UUID): The ID of the entity.

        Returns:
            bool: True if the entity was deleted, False otherwise.

        Raises:
            RepositoryError: If an unexpected error occurs.
        """
        if id not in self._storage:
            raise RecordNotFoundError(
                entity_type=self._get_entity_name(), identifier=id
            )
        try:
            del self._storage[id]
            return True
        except Exception as e:
            raise RepositoryError(
                f"Failed to delete entity {self._get_entity_name()} with ID {id}"
            ) from e

    def bulk_delete(self, filters: Dict[str, any]) -> int:
        """Deletes multiple entities matching the given filters.

        Args:
            filters (Dict[str, any]): Filtering conditions.

        Returns:
            int: The number of deleted entities.

        Raises:
            ValidationError: If no filters are provided.
            RepositoryError: If an unexpected error occurs.
        """
        if not filters:
            raise ValidationError("Filters are required for bulk delete.")

        to_delete = [
            id
            for id, entity in self._storage.items()
            if all(getattr(entity, key) == value for key, value in filters.items())
        ]

        if not to_delete:
            return 0

        try:
            for id in to_delete:
                del self._storage[id]
            return len(to_delete)
        except Exception as e:
            raise RepositoryError(
                f"Failed to bulk delete entities of type {self._get_entity_name()}"
            ) from e

    def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        filters: Optional[Dict[str, any]] = None,
    ) -> List[T]:
        """Lists entities with optional filtering, sorting, and pagination.

        Args:
            limit (int): Maximum number of entities to return.
            offset (int): Number of entities to skip.
            sort_by (Optional[str]): Column name to sort by.
            filters (Optional[Dict[str, any]]): Filtering conditions.

        Returns:
            List[T]: A list of matching entities.
        """
        entities = list(self._storage.values())

        if filters:
            entities = [
                e
                for e in entities
                if all(getattr(e, k) == v for k, v in filters.items())
            ]

        if sort_by:
            entities.sort(key=lambda x: getattr(x, sort_by))

        return entities[offset : offset + limit]

    def count(self, filters: Optional[Dict[str, any]] = None) -> int:
        """Counts the total number of entities matching the filters.

        Args:
            filters (Optional[Dict[str, any]]): Filtering conditions.

        Returns:
            int: The number of matching entities.
        """
        if not filters:
            return len(self._storage)

        return sum(
            1
            for entity in self._storage.values()
            if all(getattr(entity, k) == v for k, v in filters.items())
        )

    def _get_id(self, entity: T) -> UUID:
        """Extracts the ID from an entity.

        This method assumes that the entity has an 'id' attribute.

        Args:
            entity (T): The entity instance.

        Returns:
            UUID: The unique identifier of the entity.
        """
        return entity.id

    def _get_entity_name(self) -> str:
        """Returns the entity type name for error messages."""
        return self.__class__.__name__
