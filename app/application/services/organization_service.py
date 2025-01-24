from uuid import UUID

from app.domain.models.organization import Organization, OrganizationStatus
from app.domain.repositories.organization import OrganizationRepository
from app.application.commands.organization_commands import (
    CreateOrganization,
    SuspendOrganization,
)
from app.application.queries.organization_queries import (
    ListOrganizations,
    GetOrganization,
)


class OrganizationService:
    """Service that implements CQRS pattern for organization operations.

    This service separates command (write) and query (read) operations
    while keeping the implementation simple and centralized.
    """

    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    async def list_organizations(
        self, limit: int, offset: int, status: str = None
    ) -> tuple[list[Organization], int]:
        """List organizations using the query handler."""
        query = ListOrganizations(limit=limit, offset=offset, status=status)
        query_filter = {}
        if query.status:
            if query.status not in OrganizationStatus.__members__:
                raise ValueError("Invalid status filter")
            query_filter["status"] = OrganizationStatus[query.status]

        organizations = await self.repo.list(
            limit=query.limit, offset=query.offset, filters=query_filter
        )
        total = await self.repo.count(filters=query_filter)

        return organizations, total

    async def get_organization(self, org_id: UUID) -> Organization:
        """Get a single organization using the query handler."""
        query = GetOrganization(organization_id=org_id)
        org = await self.repo.get(query.organization_id)
        if not org:
            raise ValueError("Organization not found")
        return org

    async def create_organization(self, name: str) -> Organization:
        """Create an organization using the command handler."""
        cmd = CreateOrganization(name=name)
        org = Organization(name=cmd.name, id=cmd.id)
        await self.repo.save(org)
        return org

    async def suspend_organization(self, org_id: UUID) -> Organization:
        """Suspend an organization using the command handler."""
        cmd = SuspendOrganization(organization_id=org_id)
        org = await self.repo.get(cmd.organization_id)
        if not org:
            raise ValueError("Organization not found")
        org.suspend()
        await self.repo.save(org)
        return org
