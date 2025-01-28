from uuid import UUID

from app.core.accounts.interfaces import MerchantRepository
from app.core.accounts.models.merchant_models import Merchant


class MerchantService:
    """Service for managing merchant operations.

    This service handles the creation and management of merchants within the system.
    It provides an abstraction layer between the application layer and the merchant
    repository, implementing business logic related to merchant operations.

    Attributes:
        repo (MerchantRepository): Repository for merchant persistence operations.
    """

    def __init__(self, repo: MerchantRepository):
        """Initialize the merchant service.

        Args:
            repo: Repository instance for merchant persistence operations.
        """
        self.repo = repo

    async def create_merchant(
        self, org_id: UUID, name: str, country_code: str, currency: str
    ) -> Merchant:
        """Create a new merchant in the system.

        Creates a merchant entity associated with the specified organization and
        persists it to the database.

        Args:
            org_id: UUID of the organization this merchant belongs to.
            name: Business name of the merchant.
            country_code: Two-letter ISO country code where the merchant operates.
            currency: Three-letter ISO currency code for merchant's primary currency.

        Returns:
            The newly created merchant entity.

        Example:
            >>> merchant = await merchant_service.create_merchant(
            ...     org_id=UUID('123e4567-e89b-12d3-a456-426614174000'),
            ...     name='Acme Corp',
            ...     country_code='US',
            ...     currency='USD'
            ... )
        """
        merchant = Merchant(
            organization_id=org_id,
            name=name,
            country_code=country_code,
            currency=currency,
        )
        await self.repo.save(merchant)
        return merchant
