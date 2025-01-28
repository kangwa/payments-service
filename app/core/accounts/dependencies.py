from app.core.accounts.adapters.db.in_memory import (
    InMemoryMerchantRepository,
    InMemoryOrganizationRepository,
)
from app.core.accounts.services.merchant_service import MerchantService
from app.core.accounts.services.organization_service import OrganizationService


async def get_organization_service():
    """Create and configure the organization service.

    Returns:
        Configured OrganizationService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = InMemoryOrganizationRepository()
    return OrganizationService(repo)


async def get_merchant_service():
    """Create and configure the merchant service.

    Returns:
        Configured MerchantService instance with in-memory repository.

    Note:
        Uses singleton repository pattern to maintain consistent state.
    """
    repo = InMemoryMerchantRepository()
    return MerchantService(repo)
