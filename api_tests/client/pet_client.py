import requests

from api_tests.config import BASE_URL, TIMEOUT


class PetClient:

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def create(self, payload: dict | None) -> requests.Response:
        return self.session.post(f"{BASE_URL}/pet", json=payload, timeout=TIMEOUT)

    def get_by_id(self, pet_id: int | str) -> requests.Response:
        return self.session.get(f"{BASE_URL}/pet/{pet_id}", timeout=TIMEOUT)

    def find_by_status(self, status: str) -> requests.Response:
        return self.session.get(
            f"{BASE_URL}/pet/findByStatus",
            params={"status": status},
            timeout=TIMEOUT,
        )

    def update(self, payload: dict) -> requests.Response:
        return self.session.put(f"{BASE_URL}/pet", json=payload, timeout=TIMEOUT)

    def delete(self, pet_id: int) -> requests.Response:
        return self.session.delete(f"{BASE_URL}/pet/{pet_id}", timeout=TIMEOUT)
