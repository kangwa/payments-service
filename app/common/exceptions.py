"""Common exceptions for the domain-driven design application.

This module defines base exceptions that are used across multiple domains
and establish consistent error handling patterns.
"""


class DomainError(Exception):
    """Base exception for all domain-specific errors.

    All domain exceptions should inherit from this class to enable proper
    error handling and maintain consistent error hierarchies.

    Args:
        message: Error description message.
        code: Optional error code for error identification.
        details: Optional dictionary with error details.

    Example:
        >>> raise DomainError("Invalid operation", code="INVALID_OP")
    """

    def __init__(
        self, message: str, code: str | None = None, details: dict | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ValidationError(DomainError):
    """Base exception for domain validation failures.

    Raised when domain object validation fails or business rules are violated.

    Example:
        >>> raise ValidationError(
        ...     "Invalid email format",
        ...     code="INVALID_EMAIL",
        ...     details={"field": "email"}
        ... )
    """

    pass


class RepositoryError(DomainError):
    """Base exception for repository operations failures.

    Parent class for specific storage/persistence related errors.

    Example:
        >>> raise RepositoryError(
        ...     "Database connection failed",
        ...     code="DB_CONNECTION_ERROR"
        ... )
    """

    pass


class RecordNotFoundError(RepositoryError):
    """Exception for when a requested record does not exist.

    Raised when attempting to retrieve, update, or delete a non-existent record.

    Args:
        entity_type: Type of entity that was not found (e.g., "User", "Organization").
        identifier: The ID or key used in the lookup.

    Example:
        >>> raise RecordNotFoundError(
        ...     entity_type="User",
        ...     identifier="123",
        ...     code="USER_NOT_FOUND"
        ... )
    """

    def __init__(
        self,
        entity_type: str,
        identifier: str | int,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        message = f"{entity_type} with identifier '{identifier}' not found"
        super().__init__(
            message=message,
            code=code or f"{entity_type.upper()}_NOT_FOUND",
            details=details or {"entity_type": entity_type, "identifier": identifier},
        )


class ApplicationError(DomainError):
    """Base exception for general application errors.

    Used for errors that are not specifically validation or repository related.

    Example:
        >>> raise ApplicationError(
        ...     "Configuration error",
        ...     code="CONFIG_ERROR",
        ...     details={"missing_key": "api_key"}
        ... )
    """

    pass


class TokenError(Exception):
    """Base exception for token-related errors.

    Parent class for specific token error types. Should not be raised directly,
    but rather through one of its more specific child classes.

    Args:
        message: Error description message.
        token: Optional reference to problematic token.
        code: Optional error code for error identification.
        details: Optional dictionary with error details.
    """

    def __init__(
        self,
        message: str,
        token: str | None = None,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, code=code, details=details)
        # Only store last few characters to avoid logging full tokens
        self.token_reference = f"...{token[-8:]}" if token else None


class InvalidTokenError(TokenError):
    """Raised when a token is malformed or has invalid signature.

    Examples:
        - Token has been tampered with
        - Token has invalid format
        - Token signature verification fails

    Args:
        message: Error description.
        token: Optional reference to invalid token.
        details: Additional error context.
    """

    def __init__(
        self,
        message: str = "Invalid token format or signature",
        token: str | None = None,
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message, token=token, code="INVALID_TOKEN", details=details
        )


class ExpiredTokenError(TokenError):
    """Raised when a token has expired.

    Examples:
        - Token expiration timestamp has passed
        - Token refresh attempt after expiry

    Args:
        message: Error description.
        token: Optional reference to expired token.
        details: Additional error context.
    """

    def __init__(
        self,
        message: str = "Token has expired",
        token: str | None = None,
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message, token=token, code="EXPIRED_TOKEN", details=details
        )
