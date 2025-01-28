from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Schema for user authentication requests.

    Attributes:
        email: User's email address.
        password: User's plaintext password for authentication.
    """

    email: str
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT authentication token responses.

    Attributes:
        access_token: JWT token string for authentication.
        token_type: Type of token, always "bearer" for JWT.
    """

    access_token: str
    token_type: str
