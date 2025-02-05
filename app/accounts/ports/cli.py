from typer import Typer
from rich import print_json

from app.accounts.ports.rest.dependencies import (
    get_organization_service,
    get_user_service,
)
from app.accounts.schemas.organization_schemas import OrganizationResponse
from app.accounts.schemas.user_schemas import UserListResponse, UserResponse
from app.accounts.value_objects.password import Password
from app.common.exceptions import ValidationError
from app.common.value_objects.email import Email

accounts_app = Typer()


@accounts_app.command()
def create_user(
    email: str,
    password: str,
    organization_id: str,
):
    """Create a new user account via CLI.

    Creates a user with the provided email and password, then displays
    the created user details in JSON format.

    Args:
        email: Email address for the new user account.
        password: Password for the new user account.
        organization_id: Organization for the new user account.

    Returns:
        Prints JSON response containing user details:
            - user_id: Unique identifier
            - email: User's email address
            - status: Account status (e.g. ACTIVE)
            - created_at: Timestamp of creation
            - last_login: Last login timestamp (null for new users)

    Example:
        $ python -m app create-user --email=user@example.com --password=secret123

    Note:
        Password is sent as plaintext in CLI arguments. For better security,
        consider adding interactive password prompt in production.
    """
    user_service = get_user_service()

    user = user_service.create_user(
        email_address=email,
        plain_password=password,
        organization_id=organization_id,
    )

    response = UserResponse(
        id=user.id,
        email=user.email,
        status=user.status,
        created_at=user.created_at,
        last_login=user.last_login,
    )

    return print_json(response.model_dump_json())


@accounts_app.command()
def create_organization(
    name: str,
    domain: str,
):
    """Create a new organization account via CLI.

    Creates an organization with the provided name and domain, then displays
    the created organization details in JSON format.

    Args:
        name: Email address for the new user account.
        domain_name: Password for the new user account.

    Returns:
        Prints JSON response containing organization details:
            - id: Unique identifier
            - name: Organization name
            - domain_name: Unique Organization domain name
            =
            - created_at: Timestamp of creation
            - last_login: Last login timestamp (null for new users)

    Example:
        $ python -m app create-organization --email=user@example.com --password=secret123

    Note:
        Password is sent as plaintext in CLI arguments. For better security,
        consider adding interactive password prompt in production.
    """
    organization_service = get_organization_service()

    try:
        organization = organization_service.create_organization(
            name=name, domain=domain
        )
    except ValidationError as exc:
        print(exc.details)

    response = OrganizationResponse(
        id=organization.id,
        name=organization.name,
        status=organization.status,
        domain_name=organization.domain_name,
        created_at=organization.created_at,
        last_login=organization.last_login,
    )

    return print_json(response.model_dump_json())
