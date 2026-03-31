import pytest
from unittest.mock import Mock, ANY
from fastapi import HTTPException
from app.application.use_cases.register_user import RegisterUserUseCase
from app.presentation.schemas.user_schema import UserCreate
from app.domain.entities.user import User
from app.domain.entities.audit import AuditAction

def test_register_user_success():
    mock_user_repo = Mock()
    mock_audit_repo = Mock()
    mock_user_repo.get_by_email.return_value = None

    # Mocking saved_user
    saved_user = User(email="test@example.com", password_hash="hashed", full_name="Test")
    mock_user_repo.save.return_value = saved_user

    use_case = RegisterUserUseCase(mock_user_repo, mock_audit_repo)
    data = UserCreate(email="test@example.com", password="password123", full_name="Test User", phone="123")

    result = use_case.execute(data)

    assert result == saved_user
    mock_user_repo.get_by_email.assert_called_once_with("test@example.com")
    mock_user_repo.save.assert_called_once()

    # Verify Audit is saved
    mock_audit_repo.save.assert_called_once()
    audit_arg = mock_audit_repo.save.call_args[0][0]
    assert audit_arg.action == AuditAction.CREATE
    assert audit_arg.table_name == "users"

def test_register_user_email_exists():
    mock_user_repo = Mock()
    mock_audit_repo = Mock()
    # Mock an existing user
    existing_user = User(email="test@example.com", password_hash="hash", full_name="Existing")
    mock_user_repo.get_by_email.return_value = existing_user

    use_case = RegisterUserUseCase(mock_user_repo, mock_audit_repo)
    data = UserCreate(email="test@example.com", password="password123", full_name="Test User")

    with pytest.raises(HTTPException) as excinfo:
        use_case.execute(data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Email já registrado no sistema."
    mock_user_repo.save.assert_not_called()
    mock_audit_repo.save.assert_not_called()
