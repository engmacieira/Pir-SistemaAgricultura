import uuid
from datetime import datetime, timezone
import pytest
from app.domain.entities.user import User, UserRole

def test_user_creation():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User",
        phone="123456789"
    )

    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password"
    assert user.full_name == "Test User"
    assert user.role == UserRole.CLIENTE
    assert user.is_active is True
    assert user.is_verified is False
    assert user.id is not None
    assert user.created_at is not None

def test_user_accept_terms():
    user = User(email="test@example.com", password_hash="hash", full_name="Test")
    assert user.terms_accepted_at is None

    user.accept_terms()

    assert user.terms_accepted_at is not None
    assert user.updated_at is not None

def test_user_verify_account():
    user = User(email="test@example.com", password_hash="hash", full_name="Test")
    assert user.is_verified is False

    user.verify_account()

    assert user.is_verified is True
    assert user.updated_at is not None

def test_user_register_login():
    user = User(email="test@example.com", password_hash="hash", full_name="Test")
    assert user.last_login is None

    user.register_login()

    assert user.last_login is not None
    # register_login does not call mark_as_updated according to current implementation
    assert user.updated_at is None

def test_user_deactivate():
    user = User(email="test@example.com", password_hash="hash", full_name="Test")
    assert user.is_active is True

    user.deactivate()

    assert user.is_active is False
    assert user.updated_at is not None

def test_user_delete_account():
    user = User(email="test@example.com", password_hash="hash", full_name="Test")
    assert user.is_active is True
    assert user.deleted_at is None

    user.delete_account()

    assert user.is_active is False
    assert user.deleted_at is not None
