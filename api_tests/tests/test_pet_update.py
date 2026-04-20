import pytest
import allure
from jsonschema import validate

from api_tests.client.pet_client import PetClient
from api_tests.schemas.pet_schema import PET_RESPONSE_SCHEMA


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
@allure.story("Update")
class TestPetUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /pet — update name and status returns 200 with updated fields")
    def test_update_pet_returns_200_with_updated_fields(self, created_pet: dict) -> None:
        updated = {**created_pet, "name": "UpdatedBuddy", "status": "sold"}

        resp = self.client.update(updated)

        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "UpdatedBuddy"
        assert body["status"] == "sold"
        assert "application/json" in resp.headers.get("Content-Type", "")
        validate(instance=body, schema=PET_RESPONSE_SCHEMA)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("PUT /pet — update persists on subsequent GET")
    def test_update_pet_persists_on_get(self, created_pet: dict) -> None:
        updated = {**created_pet, "name": "PersistName", "status": "pending"}

        self.client.update(updated)
        verify_resp = self.client.get_by_id(created_pet["id"])

        assert verify_resp.status_code == 200
        body = verify_resp.json()
        assert body["name"] == "PersistName"
        assert body["status"] == "pending"
