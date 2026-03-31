"""
Core: Segurança e Dependências de Autenticação.
"""

import os
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

# O OAuth2PasswordBearer espera a URL de onde obter o token (ex: /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

from app.core.config import SECRET_KEY, ALGORITHM

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> uuid.UUID:
    """
    Decodifica o token JWT e extrai o ID do usuário (sub).
    Essa dependência garante que as rotas protegidas exijam um token válido.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        return uuid.UUID(user_id_str)

    except JWTError:
        raise credentials_exception
    except ValueError: # Caso o UUID não seja válido
        raise credentials_exception
