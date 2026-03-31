"""
Caso de Uso: Registro de Usuário.
"""

from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.domain.entities.user import User
from app.domain.entities.audit import AuditLog, AuditAction
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.audit_repository import IAuditRepository
from app.presentation.schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUserUseCase:
    """Orquestra a criação de um novo utilizador no sistema."""
    
    def __init__(self, user_repo: IUserRepository, audit_repo: IAuditRepository):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(self, data: UserCreate) -> User:
        """
        Executa a lógica de registro.
        
        Args:
            data (UserCreate): Dados validados do novo usuário.
            
        Returns:
            User: Entidade de domínio do usuário criado.
            
        Raises:
            HTTPException: Se o email já estiver em uso.
        """
        # 1. Verifica se usuário já existe
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado no sistema."
            )
            
        # 2. Cria a entidade de Domínio
        hashed_password = pwd_context.hash(data.password)
        new_user = User(
            email=data.email,
            password_hash=hashed_password,
            full_name=data.full_name,
            phone=data.phone
        )
        
        # 3. Persiste o usuário
        saved_user = self.user_repo.save(new_user)
        
        # 4. Grava na Auditoria (Gravador de Voo)
        audit_log = AuditLog(
            table_name="users",
            record_id=str(saved_user.id),
            action=AuditAction.CREATE,
            new_values={"email": saved_user.email, "full_name": saved_user.full_name}
        )
        self.audit_repo.save(audit_log)
        
        return saved_user