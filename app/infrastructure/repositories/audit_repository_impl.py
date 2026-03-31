"""
Implementação de Infraestrutura: Repositório de Auditoria (Caixa Preta).
Garante a escrita imutável de logs transacionais.
NÃO permite Updates ou Deletes lógicos/físicos.
"""

from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import IAuditRepository
from app.infrastructure.models.audit_model import AuditModel

class AuditRepositoryImpl(IAuditRepository):
    """
    Repositório focado exclusivamente em operações de inserção e leitura analítica.
    """
    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: AuditModel) -> AuditLog:
        """Converte a linha de log do banco para a entidade de leitura do domínio."""
        return AuditLog(**{c.name: getattr(model, c.name) for c in model.__table__.columns})

    def save(self, audit_log: AuditLog) -> AuditLog:
        """
        Persiste um evento no gravador de voo do sistema.
        Operação estritamente de APPEND (Inserção).
        """
        model = AuditModel(**audit_log.__dict__)
        self.session.add(model)
        self.session.commit()
        return audit_log

    def get_by_record(self, table_name: str, record_id: str) -> List[AuditLog]:
        """
        Reconstrói o histórico (Timeline) de um registro específico.
        Ex: O que aconteceu com o pedido #123 na tabela 'orders'?
        """
        models = (
            self.session.query(AuditModel)
            .filter(AuditModel.table_name == table_name)
            .filter(AuditModel.record_id == record_id)
            .order_by(AuditModel.created_at.asc()) # Retorna em ordem cronológica
            .all()
        )
        return [self._to_entity(model) for model in models]