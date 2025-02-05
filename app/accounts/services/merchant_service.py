"""Merchant service for the accounts domain.

This service handles merchant-related business operations including creation,
listing, and status management of merchant accounts.
"""

from typing import Any, Dict, List, Tuple
from uuid import UUID

from app.accounts.entities.merchant import Merchant, MerchantStatus
from app.accounts.interfaces.merchant_repo import MerchantRepository


class MerchantService:
    """Service for managing merchant operations.

    This service implements merchant management functionality including:
    - Merchant creation and validation
    - Merchant listing and filtering
    - Status management
    - Payment method configuration

    Args:
        repo: Repository for merchant persistence operations.

    Example:
        >>> merchant_service = MerchantService(repo=merchant_repo)
        >>> merchant = merchant_service.create_merchant(
        ...     org_id=org_id,
        ...     name="Acme Store",
        ...     country_code="US",
        ...     currency="USD"
        ... )
    """

    def __init__(self, repo: MerchantRepository):
        self.repo = repo

    def list_merchants(
        self, org_id: UUID, limit: int, offset: int, status: str | None = None
    ) -> Tuple[List[Merchant], int]:
        """List merchants with pagination and filtering.

        Args:
            org_id: Organization ID to filter merchants by.
            limit: Maximum number of merchants to return.
            offset: Number of merchants to skip.
            status: Optional status filter (e.g., 'ACTIVE', 'SUSPENDED').

        Returns:
            Tuple containing list of merchants and total count.

        Raises:
            ValueError: If status filter value is invalid.
        """
        query_filter: Dict[str, Any] = {"organization_id": org_id}

        if status:
            try:
                query_filter["status"] = MerchantStatus[status.upper()]
            except KeyError:
                valid_statuses = ", ".join(MerchantStatus.__members__.keys())
                raise ValueError(
                    f"Invalid status filter. Valid values are: {valid_statuses}"
                )

        merchants = self.repo.list_all(limit=limit, offset=offset, filters=query_filter)
        total = self.repo.count(filters=query_filter)

        return merchants, total

    def get_merchant(self, merchant_id: UUID) -> Merchant:
        """Retrieve a single merchant by ID.

        Args:
            merchant_id: Unique identifier of the merchant.

        Returns:
            Merchant entity if found.

        Raises:
            ValueError: If merchant is not found.
        """
        merchant = self.repo.get(merchant_id)
        if not merchant:
            raise ValueError(f"Merchant with ID {merchant_id} not found")
        return merchant

    def create_merchant(
        self, org_id: UUID, name: str, country_code: str, currency: str
    ) -> Merchant:
        """Create a new merchant.

        Args:
            org_id: Organization ID the merchant belongs to.
            name: Business name of the merchant.
            country_code: Two-letter ISO country code.
            currency: Three-letter ISO currency code.

        Returns:
            Newly created merchant entity.

        Raises:
            ValueError: If merchant creation fails validation.
        """
        merchant = Merchant(
            name=name,
            country_code=country_code.upper(),
            currency=currency.upper(),
            organization_id=org_id,
        )
        self.repo.save(merchant)
        return merchant

    def add_payment_method(self, merchant_id: UUID, payment_method: str) -> Merchant:
        """Add a payment method to a merchant.

        Args:
            merchant_id: Merchant's unique identifier.
            payment_method: Payment method code to add.

        Returns:
            Updated merchant entity.

        Raises:
            ValueError: If merchant not found or payment method invalid.
        """
        merchant = self.get_merchant(merchant_id)
        merchant.add_payment_method(payment_method)
        self.repo.save(merchant)
        return merchant

    def suspend_merchant(self, merchant_id: UUID) -> Merchant:
        """Suspend a merchant's operations.

        Args:
            merchant_id: Merchant's unique identifier.

        Returns:
            Updated merchant entity.

        Raises:
            ValueError: If merchant not found.
        """
        merchant = self.get_merchant(merchant_id)
        merchant.suspend()
        self.repo.save(merchant)
        return merchant
