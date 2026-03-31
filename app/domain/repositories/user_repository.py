from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.base_repository import IBaseRepository

class IUserRepository(IBaseRepository[User]):
    """
    Contrato específico de Usuários.
    Já herda save, get_by_id e update do IBaseRepository.
    Aqui definimos apenas o que é exclusivo desta entidade.
    """
    
    def get_by_email(self, email: str) -> Optional[User]:
        pass