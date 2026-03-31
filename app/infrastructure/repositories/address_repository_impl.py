"""
Implementação de Infraestrutura: Repositório de Endereços.
Gerencia as operações de persistência e leitura logística.
"""

import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities.address import Address
from app.domain.repositories.address_repository import IAddressRepository
from app.infrastructure.models.address_model import AddressModel

class AddressRepositoryImpl(IAddressRepository):
    """
    Implementação concreta do contrato IAddressRepository usando SQLAlchemy.
    """
    
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: AddressModel) -> Address:
        """
        Mapeia dinamicamente os atributos da coluna para a dataclass do Domínio.
        Garante que relacionamentos (ORM) não vazem para cima.
        """
        # Excluímos campos técnicos de banco (como deleted_at) na hidratação da Entidade
        data = {c.name: getattr(model, c.name) for c in model.__table__.columns if c.name != 'deleted_at'}
        return Address(**data)

    def save(self, address: Address) -> Address:
        """
        Insere um novo endereço no banco vinculado a um user_id.
        """
        model = AddressModel(**address.__dict__)
        self.session.add(model)
        self.session.commit()
        return address

    def get_by_id(self, address_id: uuid.UUID) -> Optional[Address]:
        """
        Busca um endereço específico por ID, respeitando o Soft Delete.
        """
        model = (
            self.session.query(AddressModel)
            .filter(AddressModel.id == address_id)
            .filter(AddressModel.deleted_at.is_(None))
            .first()
        )
        return self._to_entity(model) if model else None

    def get_by_user_id(self, user_id: uuid.UUID) -> List[Address]:
        """
        Busca toda a carteira de endereços ativos de um usuário.
        Útil para a listagem no checkout do carrinho de compras.
        """
        models = (
            self.session.query(AddressModel)
            .filter(AddressModel.user_id == user_id)
            .filter(AddressModel.deleted_at.is_(None)) # Apenas endereços não deletados
            .all()
        )
        return [self._to_entity(model) for model in models]

    def update(self, address: Address) -> Address:
        """
        Atualiza um endereço existente (ex: definindo como is_default=True).
        """
        model = (
            self.session.query(AddressModel)
            .filter(AddressModel.id == address.id)
            .filter(AddressModel.deleted_at.is_(None))
            .first()
        )
        if model:
            for key, value in address.__dict__.items():
                setattr(model, key, value)
            self.session.commit()
        return address