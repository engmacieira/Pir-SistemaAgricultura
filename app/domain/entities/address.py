"""
Entidade de Domínio: Address.
Gerencia as regras de negócio de endereçamento e geolocalização.
"""

import enum
import uuid
from dataclasses import dataclass
from typing import Optional
from app.domain.entities.base_entity import AuditableEntity

class AddressType(str, enum.Enum):
    RESIDENCIAL = "RESIDENCIAL"
    COMERCIAL = "COMERCIAL"
    RURAL = "RURAL"
    PONTO_ENCONTRO = "PONTO_ENCONTRO"

@dataclass(kw_only=True)
class Address(AuditableEntity):
    
    user_id: uuid.UUID
    
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    
    address_type: AddressType = AddressType.RESIDENCIAL
    label: Optional[str] = None
    complement: Optional[str] = None
    reference_point: Optional[str] = None
    
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    is_default: bool = False
    is_active: bool = True

    # --- Comportamentos (Regras de Negócio) ---

    def set_as_default(self) -> None:
        """Define este endereço como o destino padrão para as operações."""
        self.is_default = True
        self.mark_as_updated()

    def remove_default(self) -> None:
        """Remove a flag de endereço principal."""
        self.is_default = False
        self.mark_as_updated()

    def deactivate(self) -> None:
        """Inativa temporariamente um endereço, removendo-o também do status de padrão."""
        self.is_active = False
        self.is_default = False
        self.mark_as_updated()
        
    def archive(self) -> None:
        """Aplica o Soft Delete. O endereço deixa de estar disponível para novas encomendas, mas mantém-se para o histórico."""
        self.deactivate()
        self.soft_delete()