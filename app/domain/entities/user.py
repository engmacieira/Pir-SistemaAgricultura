"""
Entidade de Domínio: User.
Representa o utilizador no núcleo do sistema, contendo regras de negócio de identidade.
"""

import enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from app.domain.entities.base_entity import AuditableEntity

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    PRODUTOR = "PRODUTOR"
    CLIENTE = "CLIENTE"

@dataclass(kw_only=True)
class User(AuditableEntity): # Herda id, created_at, updated_at, deleted_at e comportamentos associados
    
    email: str
    password_hash: str
    full_name: str
    role: UserRole = UserRole.CLIENTE
    
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    is_active: bool = True
    is_verified: bool = False
    
    terms_accepted_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    # --- Comportamentos (Regras de Negócio) ---

    def accept_terms(self) -> None:
        """Registra o aceite dos termos de uso (LGPD) e marca a entidade como atualizada."""
        self.terms_accepted_at = datetime.now(timezone.utc)
        self.mark_as_updated()

    def verify_account(self) -> None:
        """Valida a conta do utilizador."""
        self.is_verified = True
        self.mark_as_updated()

    def register_login(self) -> None:
        """Atualiza a data do último login sem necessariamente disparar um 'update' geral de perfil."""
        self.last_login = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """
        Suspensão da conta (Diferente de Soft Delete).
        O utilizador não pode fazer login, mas os seus dados continuam visíveis para o sistema.
        """
        self.is_active = False
        self.mark_as_updated()
        
    def delete_account(self) -> None:
        """
        Encerramento da conta. Aplica o Soft Delete e inativa o acesso.
        """
        self.is_active = False
        self.soft_delete() # Chama o método da classe mãe (AuditableEntity)