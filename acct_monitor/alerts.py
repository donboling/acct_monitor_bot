import smtplib
from email.mime.text import MIMEText
import os

from dotenv import load_dotenv
load_dotenv()

EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM")
EMAIL_PASS = os.getenv("ALERT_EMAIL_PASSWORD")
EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print("✅ Email alert sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
