"""
Configuração do Banco de Dados e Mixins (SQLAlchemy).
Preparado para SQLite (Desenvolvimento) e PostgreSQL (Produção).
"""

import os
import sys
from sqlalchemy import create_engine, Column, DateTime, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Inicialização de ambiente
load_dotenv()

# 1. Configurações de Conexão
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agrolocal.db")

# 2. Resiliência de Engine (Adaptação Automática SQLite vs PostgreSQL)
if DATABASE_URL.startswith("sqlite"):
    # Configuração exclusiva para SQLite (Permite concorrência de threads no FastAPI)
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Configuração Enterprise para PostgreSQL
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        pool_size=50,
        max_overflow=150
    )

# 3. Gestão Transacional
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 4. Abstração de Tipos (Cross-Database)
# Utiliza o tipo Uuid do SQLAlchemy 2.0 (PostgreSQL = UUID nativo, SQLite = CHAR(32) ou String)
GUID = Uuid(as_uuid=True)

# --- Mixins de DRY e Auditoria ---

class TimestampMixin:
    """Rastreamento padronizado de criação e atualização."""
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
        doc="Data e hora em que o registro foi criado."
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        nullable=True,
        doc="Data e hora da última modificação."
    )

class SoftDeleteMixin:
    """Implementação padronizada de Exclusão Lógica."""
    deleted_at = Column(
        DateTime(timezone=True), 
        nullable=True, 
        doc="Data da exclusão lógica (Se Nulo = Registro Ativo)."
    )

def get_db():
    """Dependência para injeção da sessão de banco de dados no FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()