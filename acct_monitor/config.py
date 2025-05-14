import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("TT_USERNAME")
PASSWORD = os.getenv("TT_PASSWORD")
IS_LIVE = os.getenv("TT_IS_LIVE", "False") == "True"


# --- Configuration --- old

USE_SANDBOX = True

# Sandbox credentials
SANDBOX_USERNAME = 'ttsandboxdcb'
SANDBOX_PASSWORD = '539Xks$Zw7v^*yKQuF1y'

# Production credentials
PROD_USERNAME = 'your_production_username_here'
PROD_PASSWORD = 'your_production_password_here'

# Email config
EMAIL_FROM = 'ttsandboxdcb@gmail.com'
EMAIL_FROM_PASSWORD = 'vhyj sdmq hhpu axem'
EMAIL_TO = 'don.boling@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587