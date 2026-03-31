import uuid
import pytest
from app.domain.entities.audit import AuditLog, AuditAction

def test_audit_log_creation():
    record_id = str(uuid.uuid4())
    log = AuditLog(
        table_name="users",
        record_id=record_id,
        action=AuditAction.CREATE,
        new_values={"email": "test@example.com"}
    )

    assert log.table_name == "users"
    assert log.record_id == record_id
    assert log.action == AuditAction.CREATE
    assert log.new_values == {"email": "test@example.com"}
    assert log.id is not None
    assert log.created_at is not None

def test_audit_log_update_without_values_raises_error():
    record_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match="Violação de Integridade: A ação UPDATE exige os deltas"):
        AuditLog(
            table_name="users",
            record_id=record_id,
            action=AuditAction.UPDATE
        )

def test_audit_log_update_with_values():
    record_id = str(uuid.uuid4())
    log = AuditLog(
        table_name="users",
        record_id=record_id,
        action=AuditAction.UPDATE,
        old_values={"email": "old@example.com"},
        new_values={"email": "new@example.com"}
    )

    assert log.action == AuditAction.UPDATE
    assert log.old_values == {"email": "old@example.com"}
    assert log.new_values == {"email": "new@example.com"}

def test_audit_log_clean_ip_and_user_agent():
    log = AuditLog(
        table_name="users",
        record_id="123",
        action=AuditAction.LOGIN,
        ip_address="  192.168.0.1  ",
        user_agent="  Mozilla/5.0  "
    )

    assert log.ip_address == "192.168.0.1"
    assert log.user_agent == "Mozilla/5.0"
