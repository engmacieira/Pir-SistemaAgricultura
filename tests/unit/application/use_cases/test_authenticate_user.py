import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from app.application.use_cases.authenticate_user import AuthenticateUserUseCase, pwd_context
from app.presentation.schemas.auth_schema import LoginRequest
from app.domain.entities.user import User

def test_authenticate_user_success():
    mock_user_repo = Mock()
    mock_audit_repo = Mock()

    # Mock an existing user with correct password
    hashed_password = pwd_context.hash("password123")
    existing_user = User(email="test@example.com", password_hash=hashed_password, full_name="Test")
    mock_user_repo.get_by_email.return_value = existing_user

    use_case = AuthenticateUserUseCase(mock_user_repo, mock_audit_repo)
    request = LoginRequest(email="test@example.com", password="password123")

    result = use_case.execute(request, ip_address="127.0.0.1")

    assert result.access_token is not None
    assert type(result.access_token) == str

    mock_user_repo.update.assert_called_once_with(existing_user)
    mock_audit_repo.save.assert_called_once()
    assert existing_user.last_login is not None

def test_authenticate_user_invalid_credentials():
    mock_user_repo = Mock()
    mock_audit_repo = Mock()

    # Mock an existing user but different password
    hashed_password = pwd_context.hash("password123")
    existing_user = User(email="test@example.com", password_hash=hashed_password, full_name="Test")
    mock_user_repo.get_by_email.return_value = existing_user

    use_case = AuthenticateUserUseCase(mock_user_repo, mock_audit_repo)
    request = LoginRequest(email="test@example.com", password="wrongpassword")

    with pytest.raises(HTTPException) as excinfo:
        use_case.execute(request)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciais inválidas."
    mock_user_repo.update.assert_not_called()

def test_authenticate_user_inactive_account():
    mock_user_repo = Mock()
    mock_audit_repo = Mock()

    # Mock an inactive user
    hashed_password = pwd_context.hash("password123")
    existing_user = User(email="test@example.com", password_hash=hashed_password, full_name="Test")
    existing_user.is_active = False
    mock_user_repo.get_by_email.return_value = existing_user

    use_case = AuthenticateUserUseCase(mock_user_repo, mock_audit_repo)
    request = LoginRequest(email="test@example.com", password="password123")

    with pytest.raises(HTTPException) as excinfo:
        use_case.execute(request)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Conta inativa ou suspensa."
