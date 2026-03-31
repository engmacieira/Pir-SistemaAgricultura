"""
Router: Autenticação e Registro.
"""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.presentation.schemas.user_schema import UserCreate, UserResponse
from app.presentation.schemas.auth_schema import LoginRequest, TokenResponse
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.authenticate_user import AuthenticateUserUseCase

# Dependências (Assumindo que estão implementadas na infraestrutura)
from app.core.database import get_db 
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.audit_repository_impl import AuditRepositoryImpl

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_register_use_case(db: Session = Depends(get_db)):
    """Injeção de Dependência para o Use Case de Registro."""
    user_repo = UserRepositoryImpl(db)
    audit_repo = AuditRepositoryImpl(db)
    return RegisterUserUseCase(user_repo, audit_repo)

def get_auth_use_case(db: Session = Depends(get_db)):
    """Injeção de Dependência para o Use Case de Login."""
    user_repo = UserRepositoryImpl(db)
    audit_repo = AuditRepositoryImpl(db)
    return AuthenticateUserUseCase(user_repo, audit_repo)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: UserCreate, 
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    """Endpoint para cadastro de um novo utilizador."""
    return use_case.execute(data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    request_data: LoginRequest,
    req: Request,
    use_case: AuthenticateUserUseCase = Depends(get_auth_use_case)
):
    """Endpoint para autenticação de utilizador."""
    client_ip = req.client.host if req.client else None
    return use_case.execute(request_data, ip_address=client_ip)