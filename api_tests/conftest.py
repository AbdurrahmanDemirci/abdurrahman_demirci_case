import pytest

from api_tests.client.pet_client import PetClient
from api_tests.data.pet_data import build_pet


@pytest.fixture(scope="session")
def client() -> PetClient:
    return PetClient()


@pytest.fixture
def created_pet(client: PetClient) -> dict:
    payload = build_pet()
    resp = client.create(payload)
    assert resp.status_code == 200, f"Pet creation failed: {resp.text}"
    pet = resp.json()
    yield pet
    client.delete(pet["id"])
