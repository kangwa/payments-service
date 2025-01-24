from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.domain.models.auth import UserStatus


class LoginRequest(BaseModel):
    """Schema for user authentication requests.

    Attributes:
        email: User's email address.
        password: User's plaintext password for authentication.
    """

    email: str
    password: str


class UserCreateRequest(BaseModel):
    """Schema for user registration requests.

    Attributes:
        email: Email address for the new account. Must be valid email format.
        password: Password for the new account. Will be hashed before storage.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in API responses.

    Handles serialization of user data while excluding sensitive fields.

    Attributes:
        user_id: Unique identifier for the user.
        email: User's email address.
        status: Current account status (e.g., ACTIVE, SUSPENDED).
        created_at: Timestamp when the account was created.
        last_login: Timestamp of last successful login, null if never logged in.

    Note:
        Configured to automatically convert datetime to ISO format and
        UUID to string representation in JSON responses.
    """

    user_id: UUID
    email: EmailStr
    status: UserStatus
    created_at: datetime
    last_login: datetime | None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat(), UUID: lambda v: str(v)}


class TokenResponse(BaseModel):
    """Schema for JWT authentication token responses.

    Attributes:
        access_token: JWT token string for authentication.
        token_type: Type of token, always "bearer" for JWT.
    """

    access_token: str
    token_type: str
