from sqlmodel import Session

from app.accounts.adapters.db.sql_model.models import OrganizationORM
from app.accounts.entities.organization import Organization
from app.accounts.interfaces.organization_repo import OrganizationRepository
from app.common.adapters.db.sql_model import SQLModelRepository


class SQLModelOrganizationRepository(
    SQLModelRepository[Organization, OrganizationORM],
    OrganizationRepository,
):
    """
    SQL Model implementation of the organization repository.

    This class provides methods to interact with the SQL database for
    performing CRUD operations on Organization entities. It extends
    `SQLModelRepository` for common functionality and implements the
    `OrganizationRepository` interface.

    Attributes:
        session (Session): The SQLAlchemy session for database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The SQLAlchemy session for interacting with the database.
        """
        super().__init__(session, OrganizationORM)

    def _to_model(self, organization: Organization) -> OrganizationORM:
        """
        Convert an `Organization` domain entity to a SQLAlchemy model.

        Args:
            organization (Organization): The `Organization` domain entity to convert.

        Returns:
            OrganizationModel: The corresponding `OrganizationModel` SQLAlchemy model.
        """
        return OrganizationORM(
            id=organization.id,
            name=organization.name,
            domain=organization.domain,
            status=organization.status.value,
            created_at=organization.created_at,
            # metadata=user.metadata,
        )

    def _to_entity(self, model: OrganizationORM) -> Organization:
        """
        Convert a SQLAlchemy model to an `Organization` domain entity.

        Args:
            model (OrganizationModel): The `OrganizationModel` SQLAlchemy model to convert.

        Returns:
            Organization: The corresponding `Organization` domain entity.
        """
        return Organization(
            id=model.id,
            name=model.name,
            domain=model.domain,
            created_at=model.created_at,
            status=model.status,
            # metadata=model.metadata,
        )
