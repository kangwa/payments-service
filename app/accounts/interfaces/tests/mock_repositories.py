"""Mock repository implementations for testing."""

from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from app.accounts.entities.merchant import Merchant
from app.accounts.entities.organization import Organization
from app.accounts.entities.user import User
from app.accounts.interfaces import (
    MerchantRepository,
    OrganizationRepository,
    UserRepository,
)
from app.common.value_objects.email import Email


class MockMerchantRepository(MerchantRepository):
    """Mock implementation of MerchantRepository for testing."""

    def __init__(self) -> None:
        self.merchants: Dict[UUID, Merchant] = {}

    def get_by_id(self, id: UUID) -> Optional[Merchant]:
        return deepcopy(self.merchants.get(id))

    def list(self, limit: int = 100, offset: int = 0) -> List[Merchant]:
        merchants = list(self.merchants.values())
        return deepcopy(merchants[offset : offset + limit])

    def save(self, merchant: Merchant) -> Merchant:
        self.merchants[merchant.id] = deepcopy(merchant)
        return deepcopy(merchant)

    def delete(self, id: UUID) -> None:
        if id not in self.merchants:
            raise ValueError("Merchant not found")
        del self.merchants[id]

    def count(self) -> int:
        return len(self.merchants)

    def list_by_organization(
        self, org_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[Merchant]:
        merchants = [m for m in self.merchants.values() if m.organization_id == org_id]
        return deepcopy(merchants[offset : offset + limit])

    def search_by_name(self, name: str) -> List[Merchant]:
        return deepcopy(
            [m for m in self.merchants.values() if name.lower() in m.name.lower()]
        )


class MockOrganizationRepository(OrganizationRepository):
    """Mock implementation of OrganizationRepository for testing."""

    def __init__(self) -> None:
        self.organizations: Dict[UUID, Organization] = {}

    def get_by_id(self, id: UUID) -> Optional[Organization]:
        return deepcopy(self.organizations.get(id))

    def list(self, limit: int = 100, offset: int = 0) -> List[Organization]:
        orgs = list(self.organizations.values())
        return deepcopy(orgs[offset : offset + limit])

    def save(self, organization: Organization) -> Organization:
        self.organizations[organization.id] = deepcopy(organization)
        return deepcopy(organization)

    def delete(self, id: UUID) -> None:
        if id not in self.organizations:
            raise ValueError("Organization not found")
        del self.organizations[id]

    def count(self) -> int:
        return len(self.organizations)


class MockUserRepository(UserRepository):
    """Mock implementation of UserRepository for testing."""

    def __init__(self) -> None:
        self.users: Dict[UUID, User] = {}

    def get_by_id(self, id: UUID) -> Optional[User]:
        return deepcopy(self.users.get(id))

    def list(self, limit: int = 100, offset: int = 0) -> List[User]:
        users = list(self.users.values())
        return deepcopy(users[offset : offset + limit])

    def save(self, user: User) -> User:
        self.users[user.id] = deepcopy(user)
        return deepcopy(user)

    def delete(self, id: UUID) -> None:
        if id not in self.users:
            raise ValueError("User not found")
        del self.users[id]

    def count(self) -> int:
        return len(self.users)

    def get_by_email(self, email: Email) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return deepcopy(user)
        return None

    def update_login_time(self, user_id: UUID) -> None:
        if user_id not in self.users:
            raise ValueError("User not found")
        user = self.users[user_id]
        user.last_login = datetime.now()
