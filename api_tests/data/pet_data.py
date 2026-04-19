import time

VALID_STATUSES: list[str] = ["available", "pending", "sold"]

INVALID_PET_ID: int = 999_999_999_999
INVALID_STRING_ID: str = "not-a-valid-id"


def build_pet(
    pet_id: int | None = None,
    name: str = "TestPet",
    status: str = "available",
) -> dict:
    return {
        "id": pet_id if pet_id is not None else int(time.time() * 1000) % 10 ** 9,
        "name": name,
        "status": status,
        "photoUrls": ["https://example.com/photo.jpg"],
        "category": {"id": 1, "name": "Dogs"},
        "tags": [{"id": 1, "name": "test"}],
    }
