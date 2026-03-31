"""
Caso de Uso: Gestão de Endereços.
"""

import uuid
from typing import List
from fastapi import HTTPException, status
from app.domain.entities.address import Address, AddressType
from app.domain.repositories.address_repository import IAddressRepository
from app.presentation.schemas.address_schema import AddressCreate

class AddressManagementUseCase:
    """Orquestra o CRUD de endereços."""
    
    def __init__(self, address_repo: IAddressRepository):
        self.address_repo = address_repo

    def add_address(self, user_id: uuid.UUID, data: AddressCreate) -> Address:
        """Cria e vincula um novo endereço ao utilizador."""
        
        address = Address(
            user_id=user_id,
            street=data.street,
            number=data.number,
            neighborhood=data.neighborhood,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            address_type=AddressType(data.address_type),
            label=data.label,
            complement=data.complement,
            reference_point=data.reference_point
        )
        
        if data.is_default:
            address.set_as_default()
            # OBS: Uma melhoria futura aqui seria buscar os outros endereços
            # e remover o default deles para garantir unicidade de default.
            
        return self.address_repo.save(address)

    def get_user_addresses(self, user_id: uuid.UUID) -> List[Address]:
        """Recupera todos os endereços ativos do utilizador."""
        return self.address_repo.get_by_user_id(user_id)

    def archive_address(self, address_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """Aplica Soft Delete no endereço, validando a posse."""
        address = self.address_repo.get_by_id(address_id)
        
        if not address or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endereço não encontrado ou não pertence a este utilizador."
            )
            
        # Comportamento de domínio
        address.archive()
        self.address_repo.update(address)