"""
Fundação de Repositórios (Domínio).
Define o contrato genérico para as operações básicas de persistência.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

# T representa a Entidade de Domínio (ex: User, Address)
T = TypeVar('T')  

class IBaseRepository(ABC, Generic[T]):
    """
    Interface Genérica de Repositório.
    Garante que todos os Aggregate Roots tenham operações padronizadas (DRY).
    """
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Persiste uma nova entidade."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Optional[T]:
        """Recupera uma entidade pelo seu UUID único."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Atualiza os dados de uma entidade existente."""
        pass