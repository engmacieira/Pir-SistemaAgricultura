"""
Fundação da Camada de Domínio.
Fornece classes base puras (sem dependências de framework) para garantir o DRY
na modelagem das entidades de negócio.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

@dataclass(kw_only=True)
class AuditableEntity:
    """
    Entidade Base Auditável.
    Fornece identidade (UUID), rastreio de tempo (Timestamps) e Exclusão Lógica (Soft Delete).
    Qualquer entidade de domínio que herde desta classe ganha este comportamento automaticamente.
    """
    id: uuid.UUID = field(
        default_factory=uuid.uuid4,
        metadata={"description": "Identificador único universal (UUID v4) da entidade."}
    )
    
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        metadata={"description": "Timestamp imutável do momento exato da criação no domínio."}
    )
    
    updated_at: Optional[datetime] = field(
        default=None,
        metadata={"description": "Timestamp da última mutação de estado da entidade."}
    )
    
    deleted_at: Optional[datetime] = field(
        default=None,
        metadata={"description": "Timestamp da exclusão lógica. Se preenchido, a entidade está 'morta' para o negócio."}
    )

    def mark_as_updated(self) -> None:
        """Atualiza a data de modificação. Deve ser chamado pelas subclasses após mutações de estado."""
        self.updated_at = datetime.now(timezone.utc)

    def soft_delete(self) -> None:
        """Aplica a regra de negócio de exclusão lógica na entidade."""
        self.deleted_at = datetime.now(timezone.utc)
        self.mark_as_updated()
        
    @property
    def is_deleted(self) -> bool:
        """Verifica se a entidade sofreu exclusão lógica."""
        return self.deleted_at is not None