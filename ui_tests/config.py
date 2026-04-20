import os
from dotenv import load_dotenv

load_dotenv()

BROWSER       = os.getenv("BROWSER").lower()
HEADLESS      = os.getenv("HEADLESS").lower() == "true"
BASE_URL      = os.getenv("BASE_URL")
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT"))
