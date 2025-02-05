from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.accounts.entities.user import UserStatus


class OrganizationORM(SQLModel, table=True):
    """
    Organization model using SQLModel.

    This model represents an organization in the database. It includes
    information about the organization, such as its name, domain, status,
    and the creation timestamp. It also defines relationships to users and
    merchants.

    Attributes:
        id (UUID): The unique identifier for the organization.
        name (str): The name of the organization.
        domain (str): The domain of the organization.
        status (str): The current status of the organization.
        created_at (datetime): The timestamp when the organization was created.
        users (list["UserModel"]): A list of users associated with the organization.
        merchants (list["MerchantModel"]): A list of merchants associated with the organization.
    """

    __tablename__ = "accounts_organizations"

    id: UUID = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    domain: str = Field(unique=True)
    status: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    users: list["UserORM"] = Relationship(back_populates="organization")
    merchants: list["MerchantORM"] = Relationship(back_populates="organization")


class UserORM(SQLModel, table=True):
    """
    User model using SQLModel.

    This model represents a user in the database. It includes information
    such as the user's name, email, password, status, and the associated
    organization. It also ensures that the combination of email and
    organization is unique.

    Attributes:
        id (UUID): The unique identifier for the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        last_login_at (datetime | None): The timestamp of the user's last login.
        organization_id (UUID): The ID of the organization the user belongs to.
        created_at (datetime): The timestamp when the user was created.
        status (str): The current status of the user.
        organization (OrganizationModel | None): The organization the user belongs to.
    """

    __tablename__ = "accounts_users"

    __table_args__ = (
        UniqueConstraint("email", "organization_id", name="unique_org_user"),
    )

    id: UUID = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    email: str = Field(index=True)
    hashed_password: str
    last_login_at: datetime | None
    organization_id: UUID = Field(default=None, foreign_key="accounts_organizations.id")
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = UserStatus.ACTIVE
    organization: OrganizationORM | None = Relationship(back_populates="users")


class MerchantORM(SQLModel, table=True):
    """
    Merchant model using SQLModel.

    This model represents a merchant in the database. It includes the
    merchant's name, status, country code, currency, and associated
    organization. Additionally, it defines a relationship to the organization.

    Attributes:
        id (UUID): The unique identifier for the merchant.
        name (str): The name of the merchant.
        status (str): The current status of the merchant.
        country_code (str): The country code associated with the merchant.
        currency (str): The currency associated with the merchant.
        created_at (datetime): The timestamp when the merchant was created.
        organization_id (UUID | None): The ID of the organization the merchant belongs to.
        organization (OrganizationModel | None): The organization the merchant belongs to.
    """

    __tablename__ = "accounts_merchants"

    id: UUID = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    status: str
    country_code: str
    currency: str
    created_at: datetime = Field(default_factory=datetime.now)
    organization_id: UUID | None = Field(
        default=None, foreign_key="accounts_organizations.id"
    )

    # Relationships
    organization: OrganizationORM | None = Relationship(back_populates="merchants")
