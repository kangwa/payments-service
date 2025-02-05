from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlmodel import Session

from app.accounts.adapters.db.sql_model.models import UserORM
from app.accounts.entities.user import User
from app.accounts.interfaces.user_repo import UserRepository
from app.common.adapters.db.sql_model import SQLModelRepository
from app.common.value_objects.email import Email


class SQLModelUserRepository(SQLModelRepository[User, UserORM], UserRepository):
    """
    SQL Model implementation of the user repository.

    This class provides methods to interact with the SQL database for
    performing CRUD operations on User entities. It extends the `SQLModelRepository`
    for common functionality and implements the `UserRepository` interface.

    Attributes:
        session (Session): The SQLAlchemy session for database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The SQLAlchemy session for interacting with the database.
        """
        super().__init__(session, UserORM)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.

        This method retrieves a user entity based on the provided email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            Optional[User]: The `User` domain entity if found, otherwise `None`.
        """
        stmt = select(self.model).where(self.model.email == email)
        result = self.session.execute(stmt)
        db_model = result.scalar_one_or_none()
        return self._to_entity(db_model) if db_model else None

    def list_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[User]:
        """
        List users by organization.

        This method retrieves a list of users associated with a given
        organization, with support for pagination using limit and offset.

        Args:
            org_id (UUID): The ID of the organization to filter users by.
            limit (int): The maximum number of users to return. Defaults to 100.
            offset (int): The number of users to skip. Defaults to 0.

        Returns:
            list[User]: A list of `User` domain entities.
        """
        stmt = (
            select(self.model)
            .where(self.model.organization_id == org_id)
            .limit(limit)
            .offset(offset)
        )
        result = self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars()]

    async def update_login_time(self, user_id: UUID) -> None:
        """
        Update the last login time for a user.

        This method updates the `last_login_at` attribute of the user identified
        by the provided user ID to the current timestamp.

        Args:
            user_id (UUID): The ID of the user whose login time will be updated.
        """
        user = await self.get(user_id)
        if user:
            user.last_login_at = datetime.now()
            self.save(user)

    def _to_model(self, user: User) -> UserORM:
        """
        Convert a `User` domain entity to a SQLAlchemy model.

        Args:
            user (User): The `User` domain entity to convert.

        Returns:
            UserModel: The corresponding `UserModel` SQLAlchemy model.
        """
        return UserORM(
            id=user.id,
            email=user.email.email_address,
            name=user.name,
            status=user.status.value,
            hashed_password=user.hashed_password,
            organization_id=user.organization_id,
            created_at=user.created_at,
            last_login_at=user.last_login,
            # metadata=user.metadata,
        )

    def _to_entity(self, model: UserORM) -> User:
        """
        Convert a SQLAlchemy model to a `User` domain entity.

        Args:
            model (UserModel): The `UserModel` SQLAlchemy model to convert.

        Returns:
            User: The corresponding `User` domain entity.
        """
        return User(
            id=model.id,
            email=Email(model.email),
            name=model.name,
            hashed_password=model.hashed_password,
            organization_id=model.organization_id,
            created_at=model.created_at,
            last_login=model.last_login_at,
            # metadata=model.metadata,
        )
