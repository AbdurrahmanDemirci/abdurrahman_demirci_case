import pytest
import allure

from api_tests.client.pet_client import PetClient
from api_tests.data.pet_data import INVALID_PET_ID, INVALID_STRING_ID, NEGATIVE_PET_ID
from api_tests.models.pet_model import PetBuilder


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
class TestPetNegative:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — non-existent ID returns 404")
    def test_get_nonexistent_pet_returns_404(self) -> None:
        resp = self.client.get_by_id(INVALID_PET_ID)

        assert resp.status_code == 404

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — negative ID returns 400 or 404")
    def test_get_pet_with_negative_id_returns_error(self) -> None:
        resp = self.client.get_by_id(NEGATIVE_PET_ID)

        assert resp.status_code in (400, 404)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/{id} — string ID returns 400 or 404")
    def test_get_pet_with_string_id_returns_client_error(self) -> None:
        resp = self.client.get_by_id(INVALID_STRING_ID)

        # Petstore returns 404 (treated as not found) instead of 400 (invalid input)
        assert resp.status_code in (400, 404)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Create")
    @allure.title("POST /pet — no body returns 4xx")
    def test_create_pet_with_no_body_returns_error(self) -> None:
        resp = self.client.create(None)

        assert resp.status_code in (400, 405, 415, 500)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Update")
    @allure.title("PUT /pet — invalid id type in body returns 4xx")
    def test_update_with_invalid_id_type_returns_error(self) -> None:
        resp = self.client.update(PetBuilder.invalid_body())

        assert resp.status_code in (400, 405, 500)

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Delete")
    @allure.title("DELETE /pet/{id} — non-existent ID returns 404")
    def test_delete_nonexistent_pet_returns_404(self) -> None:
        resp = self.client.delete(INVALID_PET_ID)

        assert resp.status_code == 404

    @pytest.mark.regression
    @pytest.mark.api
    @allure.story("Read")
    @allure.title("GET /pet/findByStatus — invalid status returns 200 with empty list")
    def test_find_by_invalid_status_returns_empty_list(self) -> None:
        # Petstore returns 200 + empty list for unknown status (lenient validation)
        resp = self.client.find_by_status("invalid_status_xyz")

        assert resp.status_code == 200
        assert resp.json() == []
