import smtplib

smtp_server = "smtp.gmail.com"
port = 587
sender = "ttsandboxdcb@gmail.com"
password = "wxiq bknu cbjh lhod"  # App password ONLY
receiver = "don.boling@gmail.com"

with smtplib.SMTP(smtp_server, port) as server:
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, "Subject: Test\n\nThis is a test email.")
