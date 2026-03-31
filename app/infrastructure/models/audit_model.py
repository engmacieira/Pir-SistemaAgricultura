import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.domain.entities.audit import AuditAction

class AuditModel(Base):
    """
    Modelo de Infraestrutura: Auditoria (Caixa Preta).
    Tabela Imutável (Append-Only). Não possui Soft Delete nem Update.
    """
    __tablename__ = "audit_logs"

    id = Column(
        GUID, primary_key=True, default=uuid.uuid4, index=True,
        doc="Identificador único universal (UUID v4) do log."
    )
    
    table_name = Column(
        String(50), nullable=False, index=True,
        doc="Nome da tabela no banco de dados onde o evento ocorreu."
    )
    record_id = Column(
        String(255), nullable=False, index=True,
        doc="ID do registro afetado (String para suportar UUID ou Integers de sistemas legados)."
    )
    
    action = Column(
        SQLEnum(AuditAction), nullable=False, index=True,
        doc="Tipo de operação realizada (CREATE, UPDATE, DELETE, LOGIN, etc)."
    ) 
    
    actor_id = Column(
        GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
        doc="ID do usuário (ator) que disparou a ação. SET NULL caso o usuário seja removido (Hard Delete de LGPD)."
    ) 
    
    ip_address = Column(
        String(45), nullable=True,
        doc="Endereço IP de origem da requisição."
    )
    user_agent = Column(
        String(255), nullable=True,
        doc="Dados do navegador ou dispositivo (User-Agent string)."
    )
    
    old_values = Column(
        JSON, nullable=True,
        doc="Payload em formato JSON contendo o estado do registro ANTES da modificação."
    )
    new_values = Column(
        JSON, nullable=True,
        doc="Payload em formato JSON contendo o estado do registro APÓS a modificação."
    )
    
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), index=True,
        doc="Timestamp exato e imutável de quando o evento foi registrado pelo sistema."
    )