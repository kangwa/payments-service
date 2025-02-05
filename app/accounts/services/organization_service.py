"""Organization service for the accounts domain.

This service handles organization-related business operations including creation,
listing, and status management of organizations.
"""

import re
from typing import Any, Dict, List, Tuple
from uuid import UUID

from app.accounts.entities.organization import Organization, OrganizationStatus
from app.accounts.interfaces.organization_repo import OrganizationRepository
from app.common.exceptions import ValidationError


class OrganizationService:
    """Service that implements CQRS pattern for organization operations.

    This service implements organization management functionality including:
    - Organization creation and validation
    - Organization listing and filtering
    - Status management
    - Domain verification

    Args:
        repo: Repository for organization persistence operations.

    Example:
        >>> org_service = OrganizationService(repo=org_repo)
        >>> org = org_service.create_organization(
        ...     name="Acme Corp",
        ...     domain="acme.com"
        ... )
    """

    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    def _validate_domain(self, domain: str) -> None:
        """Validate domain format.

        Args:
            domain: Domain name to validate

        Raises:
            ValueError: If domain format is invalid
        """
        domain_pattern = r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
        if not re.match(domain_pattern, domain.lower()):
            raise ValueError("Invalid domain format")

    def _validate_name(self, name: str) -> None:
        """Validate organization name.

        Args:
            name: Organization name to validate

        Raises:
            ValueError: If name is invalid
        """
        if not name or len(name.strip()) < 2:
            raise ValueError("Organization name must be at least 2 characters")
        if len(name) > 100:
            raise ValueError("Organization name must be less than 100 characters")

    def list_organizations(
        self, limit: int, offset: int, status: str | None = None
    ) -> Tuple[List[Organization], int]:
        """List organizations with pagination and filtering.

        Args:
            limit: Maximum number of organizations to return
            offset: Number of organizations to skip
            status: Optional status filter (e.g., 'ACTIVE', 'SUSPENDED')

        Returns:
            Tuple containing list of organizations and total count

        Raises:
            ValueError: If status filter value is invalid
        """
        query_filter: Dict[str, Any] = {}

        if status:
            try:
                query_filter["status"] = OrganizationStatus[status.upper()]
            except KeyError:
                valid_statuses = ", ".join(OrganizationStatus.__members__.keys())
                raise ValueError(
                    f"Invalid status filter. Valid values are: {valid_statuses}"
                )

        organizations = self.repo.list_all(
            limit=limit, offset=offset, filters=query_filter
        )

        total = self.repo.count(filters=query_filter)

        return organizations, total

    def get_organization(self, organization_id: UUID) -> Organization:
        """Retrieve a single organization by ID.

        Args:
            organization_id: Unique identifier of the organization

        Returns:
            Organization entity if found

        Raises:
            ValueError: If organization is not found
        """
        org = self.repo.get(organization_id)
        if not org:
            raise ValueError(f"Organization with ID {organization_id} not found")
        return org

    def create_organization(self, name: str, domain: str) -> Organization:
        """Create a new organization.

        Args:
            name: Name of the organization
            domain: Domain name for the organization

        Returns:
            Newly created organization entity

        Raises:
            ValueError: If organization creation fails validation
        """
        self._validate_name(name)
        self._validate_domain(domain)

        # Check domain uniqueness
        existing = self.repo.find_one({"domain": domain.lower()})
        if existing:
            raise ValidationError(f"Organization with domain {domain} already exists")

        org = Organization(
            name=name.strip(),
            domain=domain.lower(),
        )
        self.repo.save(org)
        return org

    def update_organization(
        self, organization_id: UUID, name: str | None = None, domain: str | None = None
    ) -> Organization:
        """Update an organization's details.

        Args:
            organization_id: Organization's unique identifier
            name: Optional new name
            domain: Optional new domain

        Returns:
            Updated organization entity

        Raises:
            ValueError: If organization not found or validation fails
        """
        org = self.get_organization(organization_id)

        if name is not None:
            self._validate_name(name)
            org.name = name.strip()

        if domain is not None:
            self._validate_domain(domain)
            domain = domain.lower()
            existing = self.repo.find_by_domain(domain)
            if existing and existing.id != organization_id:
                raise ValueError(f"Organization with domain {domain} already exists")
            org.domain = domain

        self.repo.save(org)
        return org

    def suspend_organization(self, organization_id: UUID) -> Organization:
        """Suspend an organization's operations.

        This will also suspend all associated merchants.

        Args:
            organization_id: Organization's unique identifier

        Returns:
            Updated organization entity

        Raises:
            ValueError: If organization not found
        """
        org = self.get_organization(organization_id)
        org.suspend()
        self.repo.save(org)
        return org

    def reactivate_organization(self, organization_id: UUID) -> Organization:
        """Reactivate a suspended organization.

        Args:
            organization_id: Organization's unique identifier

        Returns:
            Updated organization entity

        Raises:
            ValueError: If organization not found or not suspended
        """
        org = self.get_organization(organization_id)
        if org.status != OrganizationStatus.SUSPENDED:
            raise ValueError("Can only reactivate suspended organizations")
        org.activate()
        self.repo.save(org)
        return org
