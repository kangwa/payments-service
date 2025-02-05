from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.accounts.adapters.db.sql_model.models import MerchantORM
from app.accounts.entities.merchant import Merchant
from app.accounts.interfaces.merchant_repo import MerchantRepository
from app.common.adapters.db.sql_model import SQLModelRepository


class SQLModelMerchantRepository(
    SQLModelRepository[Merchant, MerchantORM], MerchantRepository
):
    """
    SQL Model implementation of the merchant repository.

    This class provides the necessary methods to interact with the
    SQL database for performing CRUD operations on Merchant entities.
    It extends the `SQLModelRepository` for common functionality and
    implements the `MerchantRepository` interface.

    Attributes:
        session (Session): The SQLAlchemy session for database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The SQLAlchemy session for interacting with the database.
        """
        super().__init__(session, MerchantORM)

    def list_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[Merchant]:
        """
        List merchants by the organization.

        This method retrieves a list of merchants associated with a given
        organization, with support for pagination using limit and offset.

        Args:
            org_id (UUID): The ID of the organization to filter merchants by.
            limit (int): The maximum number of merchants to return. Defaults to 100.
            offset (int): The number of merchants to skip. Defaults to 0.

        Returns:
            list[Merchant]: A list of `Merchant` domain entities.
        """
        stmt = (
            select(self.model)
            .where(self.model.organization_id == org_id)
            .limit(limit)
            .offset(offset)
        )
        result = self.session.exec(stmt)
        return [self._to_entity(model) for model in result.all()]

    def search_by_name(self, name: str) -> Optional[Merchant]:
        """
        Get a merchant by its name.

        This method retrieves a merchant based on the provided name.

        Args:
            name (str): The name of the merchant to search for.

        Returns:
            Optional[Merchant]: The `Merchant` domain entity if found,
                                 otherwise `None`.
        """
        stmt = select(self.model).where(self.model.name == name)
        result = self.session.execute(stmt)
        db_model = result.scalar_one_or_none()
        return self._to_entity(db_model) if db_model else None

    def _to_model(self, merchant: Merchant) -> MerchantORM:
        """
        Convert a `Merchant` domain entity to a SQLAlchemy model.

        Args:
            merchant (Merchant): The `Merchant` domain entity to convert.

        Returns:
            MerchantModel: The corresponding `MerchantModel` SQLAlchemy model.
        """
        return MerchantORM(
            id=merchant.id,
            name=merchant.name,
            currency=merchant.currency,
            country_code=merchant.country_code,
            status=merchant.status.value,
            organization_id=merchant.organization_id,
            created_at=merchant.created_at,
        )

    def _to_entity(self, model: MerchantORM) -> Merchant:
        """
        Convert a SQLAlchemy model to a `Merchant` domain entity.

        Args:
            model (MerchantModel): The `MerchantModel` SQLAlchemy model to convert.

        Returns:
            Merchant: The corresponding `Merchant` domain entity.
        """
        return Merchant(
            id=model.id,
            name=model.name,
            currency=model.currency,
            country_code=model.country_code,
            organization_id=model.organization_id,
            created_at=model.created_at,
            status=model.status,
        )
