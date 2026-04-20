import requests

from api_tests.api.base_api import BaseAPI


class PetClient(BaseAPI):

    def create(self, payload: dict | None) -> requests.Response:
        return self._post("/pet", json=payload)

    def get_by_id(self, pet_id: int | str) -> requests.Response:
        return self._get(f"/pet/{pet_id}")

    def find_by_status(self, status: str) -> requests.Response:
        return self._get("/pet/findByStatus", params={"status": status})

    def update(self, payload: dict) -> requests.Response:
        return self._put("/pet", json=payload)

    def delete(self, pet_id: int) -> requests.Response:
        return self._delete(f"/pet/{pet_id}")
