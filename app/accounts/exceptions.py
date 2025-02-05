"""Exceptions for the accounts domain.

This module defines the exception hierarchy for the accounts domain, including:
- Authentication and token-related errors
- User-related errors
- Organization-related errors

All exceptions inherit from appropriate base classes to enable proper
error handling and maintain consistent error hierarchies.
"""

from app.common.exceptions import DomainError, RecordNotFoundError


class TokenError(DomainError):
    """Base exception for token-related errors.

    Parent class for specific token error types. Should not be raised directly,
    but rather through one of its more specific child classes.
    """

    pass


class InvalidTokenError(TokenError):
    """Raised when a token is malformed or has invalid signature.

    Examples:
        - Token has been tampered with
        - Token has invalid format
        - Token signature verification fails
    """

    pass


class ExpiredTokenError(TokenError):
    """Raised when a token has expired.

    Examples:
        - Token expiration timestamp has passed
        - Token refresh attempt after expiry
    """

    pass


class AuthenticationError(DomainError):
    """Raised when authentication fails.

    Examples:
        - Invalid credentials provided
        - Token validation fails
        - Insufficient permissions

    Usage:
        ```python
        try:
            user = await auth_service.authenticate(credentials)
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=str(e))
        ```
    """

    pass


class UserError(DomainError):
    """Base exception for user-related errors."""

    pass


class UserNotFoundError(UserError, RecordNotFoundError):
    """Exception for when a requested user does not exist.

    Raised when attempting to retrieve, update, or delete a non-existent user.
    Can be raised with either user ID or email as the identifier.

    Args:
        identifier: The user ID or email used in the lookup.
        details: Optional dictionary with additional error context.

    Example:
        >>> raise UserNotFoundError(identifier="user@example.com")
        >>> raise UserNotFoundError(identifier="123e4567-e89b-12d3-a456-426614174000")
    """

    pass


class InactiveUserError(UserError):
    """Raised when attempting operations with an inactive user.

    Examples:
        - Login attempt by suspended user
        - Action attempt by deactivated user
    """

    pass


class OrganizationError(DomainError):
    """Base exception for organization-related errors."""

    pass


class OrganizationNotFoundError(OrganizationError, RecordNotFoundError):
    """Raised when an organization cannot be found.

    Examples:
        - Organization ID does not exist
        - Domain not registered
    """

    pass


class DomainAlreadyExistsError(OrganizationError):
    """Raised when attempting to use a domain that's already registered.

    Examples:
        - Creating organization with existing domain
        - Updating organization to use taken domain
    """

    pass


class InvalidOrganizationStateError(OrganizationError):
    """Raised when attempting an invalid organization state transition.

    Examples:
        - Activating an already active organization
        - Reactivating a non-suspended organization
    """

    pass
