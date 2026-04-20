import time


def _new_id() -> int:
    return int(time.time() * 1000) % 10**9


class PetBuilder:

    @staticmethod
    def full(name: str = "TestPet", status: str = "available") -> dict:
        return {
            "id": _new_id(),
            "name": name,
            "status": status,
            "photoUrls": ["https://example.com/photo.jpg"],
            "category": {"id": 1, "name": "Dogs"},
            "tags": [{"id": 1, "name": "test"}],
        }

    @staticmethod
    def minimal(name: str = "TestPet") -> dict:
        return {
            "id": _new_id(),
            "name": name,
            "photoUrls": [],
        }

    @staticmethod
    def without_name() -> dict:
        payload = PetBuilder.full()
        del payload["name"]
        return payload

    @staticmethod
    def without_photo_urls() -> dict:
        payload = PetBuilder.full()
        del payload["photoUrls"]
        return payload

    @staticmethod
    def invalid_body() -> dict:
        return {"id": "not-a-number", "name": "Ghost", "status": "available", "photoUrls": []}
