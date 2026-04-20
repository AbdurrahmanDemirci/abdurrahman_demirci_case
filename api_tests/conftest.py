from collections.abc import Generator

import pytest

from api_tests.client.pet_client import PetClient
from api_tests.models.pet_model import PetBuilder


@pytest.fixture(scope="session")
def client() -> PetClient:
    return PetClient()


@pytest.fixture
def created_pet(client: PetClient) -> Generator[dict, None, None]:
    payload = PetBuilder.full()
    resp = client.create(payload)
    assert resp.status_code == 200, f"Pet creation failed: {resp.text}"
    pet = resp.json()
    yield pet
    client.delete(pet["id"])
