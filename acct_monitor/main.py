import asyncio
from tastytrade import User
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Configuration ---

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

# Automatically select credentials and API URL
if USE_SANDBOX:
    USERNAME = SANDBOX_USERNAME
    PASSWORD = SANDBOX_PASSWORD
    DB_FILE = 'tastytrade_sandbox.db'
else:
    USERNAME = PROD_USERNAME
    PASSWORD = PROD_PASSWORD
    DB_FILE = 'tastytrade_prod.db'


# --- Email Functions ---

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_FROM_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print("Email sent successfully.")


# --- Database Functions ---

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_type TEXT,
            margin_balance REAL,
            liquidating_equity REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS latest_positions (
            account_number TEXT,
            symbol TEXT,
            quantity REAL,
            PRIMARY KEY (account_number, symbol)
        )
    ''')
    conn.commit()
    conn.close()


def save_account_info(account):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO accounts (account_number, account_type, margin_balance, liquidating_equity)
        VALUES (?, ?, ?, ?)
    ''', (
        account.account_number,
        account.account_type,
        account.margin_balance,
        account.liquidating_equity
    ))
    conn.commit()
    conn.close()


def save_latest_positions(account_number, positions):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM latest_positions WHERE account_number = ?', (account_number,))
    for pos in positions:
        cursor.execute('''
            INSERT INTO latest_positions (account_number, symbol, quantity)
            VALUES (?, ?, ?)
        ''', (account_number, pos.symbol, pos.quantity))
    conn.commit()
    conn.close()


def detect_new_positions(account_number, positions):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT symbol, quantity FROM latest_positions WHERE account_number = ?', (account_number,))
    previous_positions = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    new_positions = []
    for pos in positions:
        symbol = pos.symbol
        quantity = pos.quantity
        if symbol not in previous_positions:
            new_positions.append(f"NEW POSITION: {symbol} x {quantity}")
        elif quantity > previous_positions[symbol]:
            new_positions.append(f"INCREASED POSITION: {symbol} x {quantity} (was {previous_positions[symbol]})")
    return new_positions


# --- Main Async Function ---

async def main():
    setup_database()

    print("Logging in...")
    user = await User.login(USERNAME, PASSWORD, is_live=not USE_SANDBOX)

    accounts = await user.get_accounts()

    all_alerts = []

    for account in accounts:
        print(f"Pulling info for account {account.account_number}")
        await account.refresh_balances()

        save_account_info(account)

        positions = await account.get_positions()

        # Detect new positions
        alerts = detect_new_positions(account.account_number, positions)
        if alerts:
            all_alerts.extend(alerts)

        save_latest_positions(account.account_number, positions)

    if all_alerts:
        alert_text = "\n".join(all_alerts)
        send_email("New Tastytrade Positions Detected", alert_text)

    print("Finished.")


# --- Script Entry ---

if __name__ == "__main__":
    asyncio.run(main())
