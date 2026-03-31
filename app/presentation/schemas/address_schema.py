"""
Schemas para a Entidade Address.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid

class AddressCreate(BaseModel):
    """Schema para registro de um novo endereço."""
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    address_type: str = "RESIDENCIAL"
    label: Optional[str] = None
    complement: Optional[str] = None
    reference_point: Optional[str] = None
    is_default: bool = False

class AddressResponse(AddressCreate):
    """Schema de resposta para um endereço."""
    id: uuid.UUID
    user_id: uuid.UUID
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)