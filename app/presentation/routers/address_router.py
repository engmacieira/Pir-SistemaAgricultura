"""
Router: Gestão de Endereços.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.presentation.schemas.address_schema import AddressCreate, AddressResponse
from app.application.use_cases.address_management import AddressManagementUseCase

# Dependências Mockadas
from app.core.database import get_db 
from app.infrastructure.repositories.address_repository_impl import AddressRepositoryImpl
from app.core.security import get_current_user_id # Função teórica que extrai o sub do JWT

router = APIRouter(prefix="/addresses", tags=["Endereços"])

def get_address_use_case(db: Session = Depends(get_db)):
    """Injeção de Dependência para o Use Case de Endereços."""
    address_repo = AddressRepositoryImpl(db)
    return AddressManagementUseCase(address_repo)


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    data: AddressCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    use_case: AddressManagementUseCase = Depends(get_address_use_case)
):
    """Adiciona um novo endereço à carteira do utilizador logado."""
    return use_case.add_address(user_id, data)


@router.get("/", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
def list_addresses(
    user_id: uuid.UUID = Depends(get_current_user_id),
    use_case: AddressManagementUseCase = Depends(get_address_use_case)
):
    """Lista todos os endereços ativos do utilizador logado."""
    return use_case.get_user_addresses(user_id)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    use_case: AddressManagementUseCase = Depends(get_address_use_case)
):
    """Arquiva (Soft Delete) um endereço existente."""
    use_case.archive_address(address_id, user_id)