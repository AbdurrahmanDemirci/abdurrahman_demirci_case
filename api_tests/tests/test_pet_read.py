import pytest
import allure
from jsonschema import validate

from api_tests.client.pet_client import PetClient
from api_tests.data.pet_data import VALID_STATUSES
from api_tests.schemas.pet_schema import PET_RESPONSE_SCHEMA


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
@allure.story("Read")
class TestPetRead:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /pet/{id} — existing pet returns 200 with matching fields")
    def test_get_pet_by_id_returns_correct_pet(self, created_pet: dict) -> None:
        resp = self.client.get_by_id(created_pet["id"])

        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == created_pet["id"]
        assert body["name"] == created_pet["name"]
        assert body["status"] == created_pet["status"]
        assert "application/json" in resp.headers.get("Content-Type", "")
        validate(instance=body, schema=PET_RESPONSE_SCHEMA)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("GET /pet/findByStatus — valid status returns 200 with a list")
    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_find_by_valid_status_returns_200(self, status: str) -> None:
        resp = self.client.find_by_status(status)

        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
