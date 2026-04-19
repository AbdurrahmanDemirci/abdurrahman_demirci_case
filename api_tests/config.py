import os

BASE_URL: str = os.getenv("API_BASE_URL", "https://petstore.swagger.io/v2")
TIMEOUT: int = int(os.getenv("API_TIMEOUT", "10"))
