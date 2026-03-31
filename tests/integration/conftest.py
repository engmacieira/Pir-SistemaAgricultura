import os

# Define a SECRET_KEY de teste na variável de ambiente antes de qualquer importação que dispare app/core/config.py
os.environ["SECRET_KEY"] = "test_super_secret_key"
os.environ["ALGORITHM"] = "HS256"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_current_user_id
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.models.address_model import AddressModel
from app.infrastructure.models.audit_model import AuditModel

# Usar SQLite em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    # Inclui o app com as dependências substituídas
    with TestClient(app) as c:
        yield c

# Fixture to mock logged-in user without needing a token
@pytest.fixture
def mock_current_user(client):
    user_id = uuid.uuid4()
    app.dependency_overrides[get_current_user_id] = lambda: user_id
    yield user_id
    app.dependency_overrides.pop(get_current_user_id, None)
