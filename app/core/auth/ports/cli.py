from async_typer import AsyncTyper
from rich import print_json

from app.core.auth.services.commands.auth_commands import CreateUserCommand
from app.core.auth.dependencies import get_user_service
from app.core.auth.schemas.user import UserResponse

auth_app = AsyncTyper()


@auth_app.async_command()
async def create_user(
    email: str,
    password: str,
):
    """Create a new user account via CLI.

    Creates a user with the provided email and password, then displays
    the created user details in JSON format.

    Args:
        email: Email address for the new user account.
        password: Password for the new user account.

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

    user = await user_service.create_user(
        CreateUserCommand(email=email, password=password)
    )

    response = UserResponse(
        user_id=user.user_id,
        email=user.email,
        status=user.status,
        created_at=user.created_at,
        last_login=user.last_login,
    )

    return print_json(response.model_dump_json())
