import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base, GUID, TimestampMixin, SoftDeleteMixin
from app.domain.entities.user import UserRole

class UserModel(Base, TimestampMixin, SoftDeleteMixin):
    """
    Modelo de Infraestrutura: Usuários.
    Armazena credenciais e estado de acesso. Herda rastreio de tempo e exclusão lógica.
    """
    __tablename__ = "users"

    id = Column(
        GUID, primary_key=True, default=uuid.uuid4, index=True,
        doc="Identificador único universal (UUID v4) do usuário."
    )
    
    email = Column(
        String(255), unique=True, index=True, nullable=False,
        doc="Endereço de e-mail utilizado para autenticação. Deve ser único."
    )
    password_hash = Column(
        String(255), nullable=False,
        doc="Hash irreversível da senha do usuário (ex: gerado via Bcrypt)."
    )
    full_name = Column(
        String(100), nullable=False,
        doc="Nome completo do usuário para exibição."
    )
    phone = Column(
        String(20), nullable=True,
        doc="Número de telefone/WhatsApp com DDI e DDD."
    )
    avatar_url = Column(
        String, nullable=True,
        doc="URL da imagem de perfil (armazenada em bucket S3/Cloud Storage)."
    )
    
    role = Column(
        SQLEnum(UserRole), default=UserRole.CLIENTE, nullable=False,
        doc="Papel de autorização do usuário (ex: ADMIN, PRODUTOR, CLIENTE)."
    )
    
    is_active = Column(
        Boolean, default=True,
        doc="Flag que bloqueia o acesso sem deletar a conta (Suspensão/Inativação)."
    )
    is_verified = Column(
        Boolean, default=False,
        doc="Flag que indica se o e-mail/telefone foi validado por token."
    )
    
    terms_accepted_at = Column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp do aceite das políticas de privacidade e termos de uso (LGPD)."
    )
    last_login = Column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp do último acesso bem-sucedido ao sistema."
    )

    # --- Relacionamentos (ORM) ---
    addresses = relationship(
        "AddressModel", 
        back_populates="user", 
        cascade="all, delete-orphan",
        doc="Lista de endereços cadastrados por este usuário."
    )