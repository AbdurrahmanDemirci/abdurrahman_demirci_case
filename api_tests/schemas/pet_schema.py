PET_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "name", "photoUrls"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string"},
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"},
        },
        "category": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
    },
}
