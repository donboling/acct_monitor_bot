import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("TT_USERNAME")
PASSWORD = os.getenv("TT_PASSWORD")
IS_LIVE = os.getenv("TT_IS_LIVE", "False") == "True"


