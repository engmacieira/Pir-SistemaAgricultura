"""
Implementação de Infraestrutura: Repositório de Usuários.
Faz a ponte entre a Entidade de Domínio (User) e o Banco de Dados (UserModel).
Garante a aplicação do Soft Delete em todas as consultas.
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.models.user_model import UserModel

class UserRepositoryImpl(IUserRepository):
    """
    Implementação concreta do contrato IUserRepository usando SQLAlchemy.
    """
    
    def __init__(self, session: Session):
        """
        Injeta a sessão do banco de dados (Unidade de Trabalho).
        """
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """
        Função utilitária (Mapeador): Converte o modelo do SQLAlchemy para a Entidade de Domínio pura.
        Isola a camada de aplicação de qualquer conhecimento sobre o ORM.
        """
        return User(
            id=model.id, 
            email=model.email, 
            password_hash=model.password_hash,
            full_name=model.full_name, 
            role=model.role, 
            phone=model.phone,
            avatar_url=model.avatar_url, 
            is_active=model.is_active,
            is_verified=model.is_verified, 
            terms_accepted_at=model.terms_accepted_at,
            last_login=model.last_login, 
            created_at=model.created_at, 
            updated_at=model.updated_at
        )

    def save(self, user: User) -> User:
        """
        Persiste um novo usuário no banco de dados.
        """
        model = UserModel(**user.__dict__)
        self.session.add(model)
        self.session.commit()
        return user

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Busca um usuário pela chave primária (UUID).
        REGRAS: Ignora registros que sofreram Soft Delete (deleted_at IS NOT NULL).
        """
        model = (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id)
            .filter(UserModel.deleted_at.is_(None)) # Filtro de Exclusão Lógica
            .first()
        )
        return self._to_entity(model) if model else None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário por e-mail (usado no processo de Autenticação/Login).
        REGRAS: Ignora registros que sofreram Soft Delete.
        """
        model = (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .filter(UserModel.deleted_at.is_(None)) # Filtro de Exclusão Lógica
            .first()
        )
        return self._to_entity(model) if model else None

    def update(self, user: User) -> User:
        """
        Atualiza os dados de um usuário existente.
        O domínio já fez as mutações (ex: user.verify_account()), aqui apenas refletimos no banco.
        """
        model = (
            self.session.query(UserModel)
            .filter(UserModel.id == user.id)
            .filter(UserModel.deleted_at.is_(None))
            .first()
        )
        
        if model:
            # Atualiza apenas campos previstos na entidade de domínio
            for key, value in user.__dict__.items():
                setattr(model, key, value)
            self.session.commit()
            
        return user