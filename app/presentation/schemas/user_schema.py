"""
Schemas para a Entidade User.
Responsável por validar os dados de entrada e formatar os dados de saída na API.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    """Schema para criação de um novo usuário."""
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None

class UserResponse(BaseModel):
    """Schema para retorno de dados do usuário, omitindo dados sensíveis."""
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: str
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)