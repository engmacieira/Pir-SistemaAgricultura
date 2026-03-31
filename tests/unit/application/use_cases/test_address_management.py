import uuid
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from app.application.use_cases.address_management import AddressManagementUseCase
from app.presentation.schemas.address_schema import AddressCreate
from app.domain.entities.address import Address, AddressType

def test_add_address():
    mock_address_repo = Mock()
    use_case = AddressManagementUseCase(mock_address_repo)

    user_id = uuid.uuid4()
    data = AddressCreate(
        street="Main St", number="123", neighborhood="Downtown",
        city="City", state="State", postal_code="12345",
        address_type=AddressType.RESIDENCIAL, is_default=True
    )

    # Mock save behavior
    saved_address = Address(
        user_id=user_id, street="Main St", number="123", neighborhood="Downtown",
        city="City", state="State", postal_code="12345"
    )
    mock_address_repo.save.return_value = saved_address

    result = use_case.add_address(user_id, data)

    assert result == saved_address
    mock_address_repo.save.assert_called_once()

    # Check if address was set to default
    saved_arg = mock_address_repo.save.call_args[0][0]
    assert saved_arg.is_default is True

def test_get_user_addresses():
    mock_address_repo = Mock()
    use_case = AddressManagementUseCase(mock_address_repo)
    user_id = uuid.uuid4()

    mock_addresses = [
        Address(user_id=user_id, street="St", number="1", neighborhood="N", city="C", state="S", postal_code="0")
    ]
    mock_address_repo.get_by_user_id.return_value = mock_addresses

    result = use_case.get_user_addresses(user_id)

    assert result == mock_addresses
    mock_address_repo.get_by_user_id.assert_called_once_with(user_id)

def test_archive_address_success():
    mock_address_repo = Mock()
    use_case = AddressManagementUseCase(mock_address_repo)

    user_id = uuid.uuid4()
    address_id = uuid.uuid4()
    existing_address = Address(user_id=user_id, street="St", number="1", neighborhood="N", city="C", state="S", postal_code="0")
    existing_address.id = address_id

    mock_address_repo.get_by_id.return_value = existing_address

    use_case.archive_address(address_id, user_id)

    assert existing_address.is_active is False
    assert existing_address.deleted_at is not None
    mock_address_repo.update.assert_called_once_with(existing_address)

def test_archive_address_not_found_or_not_owned():
    mock_address_repo = Mock()
    use_case = AddressManagementUseCase(mock_address_repo)

    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    address_id = uuid.uuid4()

    existing_address = Address(user_id=other_user_id, street="St", number="1", neighborhood="N", city="C", state="S", postal_code="0")
    existing_address.id = address_id

    mock_address_repo.get_by_id.return_value = existing_address

    with pytest.raises(HTTPException) as excinfo:
        use_case.archive_address(address_id, user_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Endereço não encontrado ou não pertence a este utilizador."
