import pytest
import allure

from api_tests.client.pet_client import PetClient
from api_tests.models.pet_model import PetBuilder


@allure.parent_suite("API Tests")
@allure.suite("Pet")
@allure.feature("Pet API")
@allure.story("Lifecycle")
class TestPetLifecycle:

    @pytest.fixture(autouse=True)
    def setup(self, client: PetClient) -> None:
        self.client = client

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    @allure.title("Pet full lifecycle — Create → Read → Update → Verify → Delete → Verify 404")
    def test_full_pet_lifecycle(self) -> None:
        payload = PetBuilder.full(name="LifecyclePet", status="available")

        # Create
        create_resp = self.client.create(payload)
        assert create_resp.status_code == 200
        pet = create_resp.json()
        pet_id = pet["id"]

        # Read
        get_resp = self.client.get_by_id(pet_id)
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "LifecyclePet"

        # Update
        updated = {**pet, "name": "UpdatedLifecyclePet", "status": "sold"}
        update_resp = self.client.update(updated)
        assert update_resp.status_code == 200

        # Verify persistence
        verify_resp = self.client.get_by_id(pet_id)
        assert verify_resp.status_code == 200
        assert verify_resp.json()["name"] == "UpdatedLifecyclePet"
        assert verify_resp.json()["status"] == "sold"

        # Delete
        delete_resp = self.client.delete(pet_id)
        assert delete_resp.status_code == 200

        # Verify 404
        final_resp = self.client.get_by_id(pet_id)
        assert final_resp.status_code == 404
