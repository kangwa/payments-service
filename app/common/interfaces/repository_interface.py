from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")  # Domain entity type


class RepositoryInterface(Generic[T]):
    """Interface that defines common repository methods for CRUD operations.

    All repository implementations must adhere to this contract.
    """

    def save(self, entity: T) -> T:
        """Saves an entity in the repository.

        Args:
            entity (T): The entity to be saved.

        Returns:
            T: The saved entity.

        Raises:
            RepositoryError: If an error occurs during save.
        """
        pass

    def bulk_save(self, entities: List[T]) -> List[T]:
        """Saves multiple entities in a single transaction.

        Args:
            entities (List[T]): List of entities to save.

        Returns:
            List[T]: The saved entities.

        Raises:
            RepositoryError: If a database error occurs.
        """
        pass

    def get(self, id: UUID) -> T:
        """Retrieves an entity by its ID.

        Args:
            id (UUID): The ID of the entity.

        Returns:
            T: The entity if found.

        Raises:
            RecordNotFoundError: If the entity does not exist.
        """
        pass

    def find_one(self, filters: Dict[str, Any]) -> Optional[T]:
        """Finds a single entity matching the provided filters.

        Args:
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            Optional[T]: The matched entity, or None.

        Raises:
            ValidationError: If no filters are provided.
        """
        pass

    def exists(self, filters: Dict[str, Any]) -> bool:
        """Checks if any entity matches the given filters.

        Args:
            filters (Dict[str, Any]): Filtering conditions.

        Returns:
            bool: True if at least one entity matches, False otherwise.

        Raises:
            ValidationError: If no filters are provided.
        """
        pass

    def delete(self, id: UUID) -> bool:
        """Deletes an entity by its ID.

        Args:
            id (UUID): The ID of the entity to delete.

        Returns:
            bool: True if the entity was deleted, False otherwise.

        Raises:
            RepositoryError: If a database error occurs.
        """
        pass

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
        pass

    def list_all(
        self,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[T]:
        """Lists entities with optional filtering, sorting, and pagination.

        Args:
            limit (int, optional): Maximum number of entities to return. Defaults to 100.
            offset (int, optional): Number of entities to skip. Defaults to 0.
            sort_by (Optional[str], optional): Column name to sort by. Defaults to None.
            filters (Optional[Dict[str, Any]], optional): Filtering conditions. Defaults to None.

        Returns:
            List[T]: A list of matching entities.

        Raises:
            ValidationError: If invalid filters are provided.
        """
        pass

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Counts the total number of entities matching the filters.

        Args:
            filters (Optional[Dict[str, Any]], optional): Filtering conditions. Defaults to None.

        Returns:
            int: The number of matching entities.

        Raises:
            ValidationError: If invalid filters are provided.
        """
        pass
