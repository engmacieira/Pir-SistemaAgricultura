import uuid
import pytest
from app.domain.entities.address import Address, AddressType

def test_address_creation():
    user_id = uuid.uuid4()
    address = Address(
        user_id=user_id,
        street="Main St",
        number="123",
        neighborhood="Downtown",
        city="Metropolis",
        state="NY",
        postal_code="10001",
        address_type=AddressType.RESIDENCIAL
    )

    assert address.user_id == user_id
    assert address.street == "Main St"
    assert address.is_default is False
    assert address.is_active is True
    assert address.address_type == AddressType.RESIDENCIAL
    assert address.id is not None

def test_address_set_as_default():
    address = Address(
        user_id=uuid.uuid4(), street="St", number="1", neighborhood="N",
        city="C", state="S", postal_code="000"
    )
    assert address.is_default is False

    address.set_as_default()

    assert address.is_default is True
    assert address.updated_at is not None

def test_address_remove_default():
    address = Address(
        user_id=uuid.uuid4(), street="St", number="1", neighborhood="N",
        city="C", state="S", postal_code="000", is_default=True
    )
    assert address.is_default is True

    address.remove_default()

    assert address.is_default is False
    assert address.updated_at is not None

def test_address_deactivate():
    address = Address(
        user_id=uuid.uuid4(), street="St", number="1", neighborhood="N",
        city="C", state="S", postal_code="000", is_default=True
    )
    assert address.is_active is True
    assert address.is_default is True

    address.deactivate()

    assert address.is_active is False
    assert address.is_default is False
    assert address.updated_at is not None

def test_address_archive():
    address = Address(
        user_id=uuid.uuid4(), street="St", number="1", neighborhood="N",
        city="C", state="S", postal_code="000", is_default=True
    )
    assert address.is_active is True
    assert address.deleted_at is None

    address.archive()

    assert address.is_active is False
    assert address.deleted_at is not None
