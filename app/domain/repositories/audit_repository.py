"""
Contrato de Domínio: Repositório de Auditoria (Caixa Preta).
NÃO HERDA de IBaseRepository para garantir a imutabilidade por design.
Logs não sofrem 'update' nem exclusão.
"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.audit import AuditLog

class IAuditRepository(ABC):
    """
    Contrato estrito para o gravador de voo do sistema.
    Operações limitadas a Append (Inserção) e Leitura Analítica.
    """
    
    @abstractmethod
    def save(self, audit_log: AuditLog) -> AuditLog:
        """Persiste um novo evento de forma imutável."""
        pass

    @abstractmethod
    def get_by_record(self, table_name: str, record_id: str) -> List[AuditLog]:
        """Recupera o histórico cronológico completo de um registro específico."""
        pass