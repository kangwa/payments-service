from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List


class MerchantStatus(str, Enum):
    """Merchant status enumeration.

    Attributes:
        ACTIVE: Merchant is operational and can process transactions
        SUSPENDED: Merchant operations are temporarily suspended
        UNDER_REVIEW: Merchant is under review for compliance or other reasons
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    UNDER_REVIEW = "under_review"


class Merchant(BaseModel):
    """Merchant model representing a business entity within an organization that can process payments.

    Attributes:
        id (UUID): Unique identifier for the merchant
        organization_id (UUID): ID of the parent organization
        name (str): Business name of the merchant
        description (Optional[str]): Brief description of the merchant's business
        country_code (str): ISO country code where merchant is registered
        currency (str): Primary currency for merchant transactions
        created_at (datetime): Timestamp of merchant creation
        updated_at (datetime): Timestamp of last update
        status (MerchantStatus): Current operational status
        payment_methods (List[str]): Supported payment method codes
        api_keys (List[UUID]): List of API keys assigned to the merchant
        metadata (dict): Additional merchant metadata
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

    def suspend(self) -> None:
        """Suspend the merchant's operations.

        Sets status to SUSPENDED and updates the updated_at timestamp.
        """
        self.status = MerchantStatus.SUSPENDED
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate the merchant's operations.

        Sets status to ACTIVE and updates the updated_at timestamp.
        """
        self.status = MerchantStatus.ACTIVE
        self.updated_at = datetime.now()

    def put_under_review(self) -> None:
        """Put merchant under review.

        Sets status to UNDER_REVIEW and updates the updated_at timestamp.
        """
        self.status = MerchantStatus.UNDER_REVIEW
        self.updated_at = datetime.now()

    def add_payment_method(self, method: str) -> None:
        """Add a new payment method.

        Args:
            method (str): Payment method code to add

        Raises:
            ValueError: If payment method already exists
        """
        if method in self.payment_methods:
            raise ValueError(f"Payment method {method} already exists")
        self.payment_methods.append(method)
        self.updated_at = datetime.now()

    def remove_payment_method(self, method: str) -> None:
        """Remove a payment method.

        Args:
            method (str): Payment method code to remove

        Raises:
            ValueError: If payment method doesn't exist
        """
        if method not in self.payment_methods:
            raise ValueError(f"Payment method {method} not found")
        self.payment_methods.remove(method)
        self.updated_at = datetime.now()

    def add_api_key(self, api_key: UUID) -> None:
        """Add a new API key.

        Args:
            api_key (UUID): API key to add

        Raises:
            ValueError: If API key already exists
        """
        if api_key in self.api_keys:
            raise ValueError(f"API key {api_key} already exists")
        self.api_keys.append(api_key)
        self.updated_at = datetime.now()

    def remove_api_key(self, api_key: UUID) -> None:
        """Remove an API key.

        Args:
            api_key (UUID): API key to remove

        Raises:
            ValueError: If API key doesn't exist
        """
        if api_key not in self.api_keys:
            raise ValueError(f"API key {api_key} not found")
        self.api_keys.remove(api_key)
        self.updated_at = datetime.now()
