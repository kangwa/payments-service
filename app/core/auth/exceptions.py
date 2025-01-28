class TokenError(Exception):
    """Base exception for token-related errors.

    Parent class for specific token error types. Should not be raised directly,
    but rather through one of its more specific child classes.
    """

    pass


class InvalidTokenError(TokenError):
    """Exception raised when a token is malformed or has invalid signature.

    This exception is raised when token validation fails due to issues like
    invalid format, tampering, or incorrect signature.
    """

    pass


class ExpiredTokenError(TokenError):
    """Exception raised when a token has expired.

    This exception is raised when an otherwise valid token's expiration
    timestamp indicates it is no longer valid.
    """

    pass


class AuthenticationError(Exception):
    """Exception raised for authentication-related errors.

    This exception is used when authentication fails due to issues like
    invalid credentials, token problems, or insufficient permissions.

    Example:
        ```python
        try:
            user = await auth_service.get_current_user(token)
        except AuthenticationError as e:
            # Handle authentication failure
            raise HTTPException(status_code=401, detail=str(e))
        ```
    """

    pass
