"""
Contrato de Domínio: Repositório de Endereços.
Herda as operações básicas de IBaseRepository (save, get_by_id, update).
"""

import uuid
from typing import List
from app.domain.entities.address import Address
from app.domain.repositories.base_repository import IBaseRepository

class IAddressRepository(IBaseRepository[Address]):
    """
    Define as operações de persistência exclusivas para a entidade Address.
    As operações de save, update e get_by_id já estão garantidas pela interface base.
    """
    
    def get_by_user_id(self, user_id: uuid.UUID) -> List[Address]:
        """
        Recupera toda a carteira de endereços logísticos ativos de um usuário.
        """
        pass