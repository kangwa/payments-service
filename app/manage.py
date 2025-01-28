"""Management CLI for Payment Gateway microservice.

This module provides command-line tools for managing the Payment Gateway service,
including user management, authentication, and service configuration.

Available Commands:
   auth: User authentication and management commands
   version: Display current service version

Usage:
    python app/manage.py auth create-user test@example.com password

Note:
   This CLI is intended for administrative tasks and should be used
   with appropriate permissions in your deployment environment.
"""

import typer
from rich import print
from app.core.auth.ports.cli import auth_app
from app.core.accounts.ports.cli import accounts_app

app = typer.Typer(
    help="Management CLI for Payment Gateway microservice",
    no_args_is_help=True,
)

app.add_typer(
    auth_app,
    name="auth",
    help="User authentication and management commands",
)

app.add_typer(
    accounts_app,
    name="accounts",
    help="Organization and merchant management commands",
)


@app.command()
def version():
    """Display the current version of the payment gateway service."""
    print("v0.0.1")


if __name__ == "__main__":
    app()
