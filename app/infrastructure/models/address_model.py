import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base, GUID, TimestampMixin, SoftDeleteMixin
from app.domain.entities.address import AddressType

class AddressModel(Base, TimestampMixin, SoftDeleteMixin):
    """
    Modelo de Infraestrutura: Endereços.
    Gerencia dados logísticos, herda timestamps e soft delete.
    """
    __tablename__ = "addresses"

    id = Column(
        GUID, primary_key=True, default=uuid.uuid4, index=True,
        doc="Identificador único universal (UUID v4) do endereço."
    )
    user_id = Column(
        GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True,
        doc="Chave estrangeira vinculando este endereço a um usuário específico."
    )
    
    address_type = Column(
        SQLEnum(AddressType), default=AddressType.RESIDENCIAL,
        doc="Classificação da finalidade logística (Residencial, Comercial, Rural, etc)."
    )
    label = Column(
        String(50), nullable=True,
        doc="Apelido customizado pelo usuário (ex: 'Casa da Mãe', 'Sítio Principal')."
    )
    
    street = Column(String(150), nullable=False, doc="Logradouro (Rua, Avenida, Estrada).")        
    number = Column(String(20), nullable=False, doc="Número do local ou 'S/N'.")
    complement = Column(String(100), nullable=True, doc="Complemento (Apto, Bloco, Lote).")     
    neighborhood = Column(String(100), nullable=False, doc="Bairro ou Distrito.")  
    city = Column(String(100), nullable=False, doc="Município.")          
    state = Column(String(2), nullable=False, doc="Unidade Federativa (Sigla de 2 letras).")
    postal_code = Column(String(9), nullable=False, doc="Código de Endereçamento Postal (CEP).")
    
    reference_point = Column(String(255), nullable=True, doc="Ponto de referência para facilitar a logística.") 
    latitude = Column(Float, nullable=True, doc="Coordenada geográfica: Latitude (Útil para área rural).")
    longitude = Column(Float, nullable=True, doc="Coordenada geográfica: Longitude (Útil para área rural).")
    
    is_default = Column(
        Boolean, default=False,
        doc="Flag indicando se este é o endereço padrão de entrega/cobrança do usuário."
    )
    is_active = Column(
        Boolean, default=True,
        doc="Flag para desativar endereços antigos sem excluí-los do histórico de compras."
    )

    # --- Relacionamentos (ORM) ---
    user = relationship(
        "UserModel", 
        back_populates="addresses",
        doc="Acesso à entidade do Usuário proprietário deste endereço."
    )