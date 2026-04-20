import pytest
import allure
from jsonschema import validate

from api_tests.client.pet_client import PetClient
from api_tests.models.pet_model import PetBuilder
from api_tests.schemas.pet_schema import PET_RESPONSE_SCHEMA


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
@allure.story("Create")
class TestPetCreate:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /pet — valid payload returns 200 with correct fields")
    def test_create_pet_returns_200_and_correct_fields(self) -> None:
        payload = PetBuilder.full(name="Buddy", status="available")

        resp = self.client.create(payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == payload["id"]
        assert body["name"] == payload["name"]
        assert body["status"] == payload["status"]
        assert "application/json" in resp.headers.get("Content-Type", "")
        validate(instance=body, schema=PET_RESPONSE_SCHEMA)

        self.client.delete(body["id"])

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("POST /pet — minimal payload (name + photoUrls) returns 200")
    def test_create_minimal_pet_returns_200(self) -> None:
        payload = PetBuilder.minimal(name="MinimalPet")

        resp = self.client.create(payload)

        assert resp.status_code == 200
        self.client.delete(resp.json()["id"])
