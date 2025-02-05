from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class MerchantStatus(str, Enum):
    """Domain enumeration representing the operational states of a Merchant.

    The status determines what business operations a merchant can perform and
    is controlled through domain operations on the Merchant entity.

    Args:
        ACTIVE: Merchant is fully operational and can process transactions
        SUSPENDED: Merchant operations are temporarily halted
        UNDER_REVIEW: Merchant is undergoing compliance checks
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    UNDER_REVIEW = "under_review"


class Merchant(BaseModel):
    """Root entity representing a business that processes financial transactions.

    This aggregate root enforces business rules around merchant operations,
    payment method configurations, and API access management. It maintains its
    own consistency and serves as a transactional boundary.

    Args:
        id: Unique entity identifier, auto-generated if not provided.
        organization_id: Reference to parent organization aggregate.
        name: Legal business name for the merchant.
        description: Optional business description text.
        country_code: ISO 3166-1 alpha-2 country code (e.g., 'US').
        currency: ISO 4217 transaction currency code (e.g., 'USD').
        created_at: Timestamp of entity creation.
        updated_at: Timestamp of last modification.
        status: Current operational state from MerchantStatus.
        payment_methods: List of enabled payment processor codes.
        api_keys: List of active API authentication credentials.
        metadata: Additional context data for extensibility.

    Example:
        >>> merchant = Merchant(
        ...     name="Acme Payments",
        ...     organization_id=uuid4(),
        ...     country_code="US",
        ...     currency="USD"
        ... )
        >>> merchant.add_payment_method("stripe")
        >>> merchant.status
        <MerchantStatus.ACTIVE>
    """

    id: UUID = Field(default_factory=uuid4)
    organization_id: UUID
    name: str
    description: Optional[str] = None
    country_code: str
    currency: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: MerchantStatus = MerchantStatus.ACTIVE
    payment_methods: List[str] = Field(default_factory=list)
    api_keys: List[UUID] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

    @field_validator("country_code")
    def validate_country_code(cls, v: str) -> str:
        """Validate country code format.

        Args:
            v: Country code to validate.

        Returns:
            Validated uppercase country code.

        Raises:
            ValueError: If code is not 2 letters.
        """
        if not v.isalpha() or len(v) != 2:
            raise ValueError("Country code must be ISO 3166-1 alpha-2 format")
        return v.upper()

    @field_validator("currency")
    def validate_currency(cls, v: str) -> str:
        """Validate currency code format.

        Args:
            v: Currency code to validate.

        Returns:
            Validated uppercase currency code.

        Raises:
            ValueError: If code is not 3 letters.
        """
        if not v.isalpha() or len(v) != 3:
            raise ValueError("Currency must be ISO 4217 format")
        return v.upper()

    def suspend(self) -> None:
        """Suspend merchant operations immediately.

        Transitions status to SUSPENDED and records modification timestamp.
        Suspended merchants cannot process transactions or modify configuration.
        """
        self.status = MerchantStatus.SUSPENDED
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Restore merchant to active operational state.

        Transitions status to ACTIVE and records modification timestamp.
        Requires compliance checks to be current before activation.
        """
        self.status = MerchantStatus.ACTIVE
        self.updated_at = datetime.now()

    def put_under_review(self) -> None:
        """Initiate compliance review process.

        Transitions status to UNDER_REVIEW and records modification timestamp.
        Automatic system checks and manual verification will be triggered.
        """
        self.status = MerchantStatus.UNDER_REVIEW
        self.updated_at = datetime.now()

    def add_payment_method(self, method: str) -> None:
        """Enable a new payment processing capability.

        Args:
            method: Payment processor code (e.g., "stripe", "paypal").

        Raises:
            ValueError: If method already enabled.
        """
        if method in self.payment_methods:
            raise ValueError(f"Payment method {method} already exists")
        self.payment_methods.append(method.lower())
        self.updated_at = datetime.now()

    def remove_payment_method(self, method: str) -> None:
        """Disable a payment processing capability.

        Args:
            method: Payment processor code to disable.

        Raises:
            ValueError: If method not currently enabled.
        """
        if method not in self.payment_methods:
            raise ValueError(f"Payment method {method} not found")
        self.payment_methods.remove(method.lower())
        self.updated_at = datetime.now()

    def add_api_key(self, api_key: UUID) -> None:
        """Issue new API access credential.

        Args:
            api_key: UUID generated by the authentication system.

        Raises:
            ValueError: If key already exists.
        """
        if api_key in self.api_keys:
            raise ValueError(f"API key {api_key} already exists")
        self.api_keys.append(api_key)
        self.updated_at = datetime.now()

    def remove_api_key(self, api_key: UUID) -> None:
        """Revoke API access credential.

        Args:
            api_key: UUID of key to revoke.

        Raises:
            ValueError: If key not found.
        """
        if api_key not in self.api_keys:
            raise ValueError(f"API key {api_key} not found")
        self.api_keys.remove(api_key)
        self.updated_at = datetime.now()

    @property
    def is_active(self) -> bool:
        """Check if merchant is in active status.

        Returns:
            True if status is ACTIVE, False otherwise.
        """
        return self.status == MerchantStatus.ACTIVE
