import pytest
import allure

from api_tests.client.pet_client import PetClient
from api_tests.models.pet_model import PetBuilder


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
@allure.story("Delete")
class TestPetDelete:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /pet/{id} — returns 200, subsequent GET returns 404")
    def test_delete_pet_returns_200_then_get_returns_404(self) -> None:
        pet_id = self.client.create(PetBuilder.full(name="ToDelete")).json()["id"]

        delete_resp = self.client.delete(pet_id)
        assert delete_resp.status_code == 200

        get_resp = self.client.get_by_id(pet_id)
        assert get_resp.status_code == 404

    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("DELETE /pet/{id} — second delete on same ID returns 404 (idempotency)")
    def test_delete_pet_is_idempotent(self) -> None:
        pet_id = self.client.create(PetBuilder.full(name="IdempotentPet")).json()["id"]

        first = self.client.delete(pet_id)
        assert first.status_code == 200

        second = self.client.delete(pet_id)
        assert second.status_code == 404
