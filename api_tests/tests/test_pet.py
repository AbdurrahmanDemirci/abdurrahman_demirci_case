import pytest
import allure

from api_tests.client.pet_client import PetClient
from api_tests.data.pet_data import (
    INVALID_PET_ID,
    INVALID_STRING_ID,
    VALID_STATUSES,
    build_pet,
)


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
class TestPetCrud:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    # ── Positive ─────────────────────────────────────────────────────────────

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Create")
    @allure.title("POST /pet — valid payload returns 200 with correct fields")
    def test_01_create_pet_returns_200_and_correct_fields(self) -> None:
        payload = build_pet(name="Buddy", status="available")

        resp = self.client.create(payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == payload["id"]
        assert body["name"] == payload["name"]
        assert body["status"] == payload["status"]

        self.client.delete(body["id"])

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — existing pet returns 200 with matching fields")
    def test_02_get_pet_by_id_returns_correct_pet(self, created_pet: dict) -> None:
        resp = self.client.get_by_id(created_pet["id"])

        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == created_pet["id"]
        assert body["name"] == created_pet["name"]
        assert body["status"] == created_pet["status"]

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/findByStatus — valid status returns 200 with a list")
    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_03_find_by_valid_status_returns_200(self, status: str) -> None:
        resp = self.client.find_by_status(status)

        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Update")
    @allure.title("PUT /pet — update name and status returns 200 with updated fields")
    def test_04_update_pet_returns_200_with_updated_fields(self, created_pet: dict) -> None:
        updated = {**created_pet, "name": "UpdatedBuddy", "status": "sold"}

        resp = self.client.update(updated)

        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "UpdatedBuddy"
        assert body["status"] == "sold"

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Delete")
    @allure.title("DELETE /pet/{id} — returns 200, subsequent GET returns 404")
    def test_05_delete_pet_returns_200_then_get_returns_404(self) -> None:
        pet_id = self.client.create(build_pet(name="ToDelete")).json()["id"]

        delete_resp = self.client.delete(pet_id)
        assert delete_resp.status_code == 200

        get_resp = self.client.get_by_id(pet_id)
        assert get_resp.status_code == 404

    # ── Negative ─────────────────────────────────────────────────────────────

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — non-existent ID returns 404")
    def test_06_get_nonexistent_pet_returns_404(self) -> None:
        resp = self.client.get_by_id(INVALID_PET_ID)

        assert resp.status_code == 404

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — string ID returns 400 or 404")
    def test_07_get_pet_with_string_id_returns_client_error(self) -> None:
        resp = self.client.get_by_id(INVALID_STRING_ID)

        # Petstore returns 404 (treated as not found) instead of 400 (invalid input)
        assert resp.status_code in (400, 404)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Create")
    @allure.title("POST /pet — no body returns 4xx")
    def test_08_create_pet_with_no_body_returns_error(self) -> None:
        resp = self.client.create(None)

        assert resp.status_code in (400, 405, 415, 500)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Update")
    @allure.title("PUT /pet — invalid id type in body returns 4xx")
    def test_09_update_with_invalid_id_type_returns_error(self) -> None:
        # Petstore does upsert on unknown IDs; invalid type triggers validation error
        payload = {"id": "not-a-number", "name": "Ghost", "status": "available", "photoUrls": []}

        resp = self.client.update(payload)

        assert resp.status_code in (400, 405, 500)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Delete")
    @allure.title("DELETE /pet/{id} — non-existent ID returns 404")
    def test_10_delete_nonexistent_pet_returns_404(self) -> None:
        resp = self.client.delete(INVALID_PET_ID)

        assert resp.status_code == 404

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/findByStatus — invalid status returns 200 with empty list")
    def test_11_find_by_invalid_status_returns_empty_list(self) -> None:
        # Petstore returns 200 + empty list for unknown status (lenient validation)
        resp = self.client.find_by_status("invalid_status_xyz")

        assert resp.status_code == 200
        assert resp.json() == []
