import os
from dotenv import load_dotenv

load_dotenv()

BROWSER       = os.getenv("BROWSER", "chrome").lower()
HEADLESS      = os.getenv("HEADLESS", "false").lower() == "true"
BASE_URL      = os.getenv("BASE_URL", "https://insiderone.com")
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "30"))
