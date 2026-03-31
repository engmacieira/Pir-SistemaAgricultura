"""
Schemas para Autenticação.
"""

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Schema de requisição para login."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Schema de resposta com o Token JWT."""
    access_token: str
    token_type: str = "bearer"