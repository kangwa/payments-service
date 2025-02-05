"""Authentication schemas for the accounts domain.

This module provides Pydantic models for handling authentication-related
requests and responses, including login, token generation, and validation.
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Schema for user authentication requests.

    Args:
        email: User's email address for authentication.
        password: User's plaintext password for verification.

    Example:
        >>> request = LoginRequest(
        ...     email="user@example.com",
        ...     password="SecurePass123!"
        ... )
    """

    email: EmailStr = Field(
        ...,
        description="Email address for authentication",
        json_schema_extra={"example": "user@example.com"},  # Updated
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User's password",
        json_schema_extra={"example": "SecurePass123!"},  # Updated
    )

    model_config = {
        "json_schema_extra": {
            "example": {"email": "user@example.com", "password": "SecurePass123!"}
        }
    }


class TokenResponse(BaseModel):
    """Schema for JWT authentication token responses.

    Args:
        access_token: JWT token string for API authentication.
        token_type: Token type identifier (always "bearer").

    Example:
        >>> response = TokenResponse(
        ...     access_token="eyJ0eXAiOiJKV1QiLCJhbGci...",
        ...     token_type="bearer"
        ... )
    """

    access_token: str = Field(
        ...,
        description="JWT access token",
        json_schema_extra={"example": "eyJ0eXAiOiJKV1QiLCJhbGci..."},  # Updated
    )
    token_type: str = Field(
        default="bearer",
        description="Token type, always 'bearer'",
        json_schema_extra={"example": "bearer"},  # Updated
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
                "token_type": "bearer",
            }
        }
    }
