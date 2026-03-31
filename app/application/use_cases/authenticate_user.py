"""
Caso de Uso: Autenticação de Usuário (Login).
"""

import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from app.domain.entities.audit import AuditLog, AuditAction
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.audit_repository import IAuditRepository
from app.presentation.schemas.auth_schema import LoginRequest, TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthenticateUserUseCase:
    """Orquestra o login e a emissão do JWT."""
    
    def __init__(self, user_repo: IUserRepository, audit_repo: IAuditRepository):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(self, request: LoginRequest, ip_address: str = None) -> TokenResponse:
        """
        Verifica credenciais e gera o token de acesso.
        
        Args:
            request (LoginRequest): Credenciais do usuário.
            ip_address (str): IP da requisição para auditoria.
            
        Returns:
            TokenResponse: Token JWT gerado.
        """
        # 1. Busca usuário
        user = self.user_repo.get_by_email(request.email)
        if not user or not pwd_context.verify(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Conta inativa ou suspensa."
            )

        # 2. Atualiza comportamento de domínio (Último Login)
        user.register_login()
        self.user_repo.update(user)
        
        # 3. Auditoria
        audit_log = AuditLog(
            table_name="users",
            record_id=str(user.id),
            action=AuditAction.LOGIN,
            actor_id=user.id,
            ip_address=ip_address
        )
        self.audit_repo.save(audit_log)

        # 4. Gera Token JWT
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(user.id), "exp": expire, "role": user.role}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return TokenResponse(access_token=encoded_jwt)