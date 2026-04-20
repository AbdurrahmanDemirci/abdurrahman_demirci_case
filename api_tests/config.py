import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("API_BASE_URL")
TIMEOUT: int = int(os.getenv("API_TIMEOUT"))
