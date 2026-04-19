import os
from dotenv import load_dotenv

load_dotenv()

BROWSER         = os.getenv("BROWSER", "chrome").lower()
HEADLESS        = os.getenv("HEADLESS", "false").lower() == "true"
BASE_URL        = os.getenv("BASE_URL", "https://insiderone.com")
CAREERS_URL     = os.getenv("CAREERS_URL", "https://insiderone.com/careers/#open-roles")
EXPLICIT_WAIT   = int(os.getenv("EXPLICIT_WAIT", "30"))
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "automation-test-results/screenshots")
