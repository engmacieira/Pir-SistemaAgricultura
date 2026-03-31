"""
Entidade de Domínio: AuditLog.
O Gravador de Voo do sistema. Entidade imutável (Append-Only).
Não herda de AuditableEntity pois não sofre mutações nem exclusões.
"""

import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone

class AuditAction(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    SYSTEM_EVENT = "SYSTEM_EVENT"

@dataclass(kw_only=True)
class AuditLog:
    """Registo estrito de eventos no sistema."""
    
    table_name: str
    record_id: str
    action: AuditAction
    
    actor_id: Optional[uuid.UUID] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    old_values: Optional[Dict[str, Any]] = None 
    new_values: Optional[Dict[str, Any]] = None
    
    # Identidade e Tempo Imutável
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Validação de Integridade de Domínio no momento da instância."""
        
        if self.action == AuditAction.UPDATE and (self.old_values is None or self.new_values is None):
            raise ValueError("Violação de Integridade: A ação UPDATE exige os deltas 'old_values' e 'new_values'.")
            
        if self.ip_address:
            self.ip_address = str(self.ip_address).strip() or None
            
        if self.user_agent:
            self.user_agent = str(self.user_agent).strip() or None