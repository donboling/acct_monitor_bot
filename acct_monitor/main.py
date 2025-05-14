import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from tastytrade import Session, Account
from alerts import send_email

# Load environment variables
load_dotenv()

USERNAME = os.getenv("TT_USERNAME")
PASSWORD = os.getenv("TT_PASSWORD")
IS_LIVE = os.getenv("TT_IS_LIVE", "False").lower() == "true"

DB_FILE = "acct_monitor.db"

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_type TEXT,
            margin_balance REAL,
            liquidating_equity REAL,
            timestamp DATETIME
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            symbol TEXT,
            quantity REAL,
            instrument_type TEXT,
            market_value REAL,
            timestamp DATETIME
        )
    ''')

    conn.commit()
    conn.close()

# --- Save snapshot ---
def save_snapshot(account, balances, positions):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    timestamp = datetime.now().isoformat()

    cur.execute('''
        INSERT OR REPLACE INTO accounts
        (account_number, account_type, margin_balance, liquidating_equity, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        account.account_number,
        account.account_type_name,
        float(balances.margin_equity),
        float(balances.net_liquidating_value),
        timestamp
    ))

    for pos in positions:
        cur.execute('''
            INSERT INTO positions
            (account_number, symbol, quantity, instrument_type, market_value, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            account.account_number,
            pos.symbol,
            float(pos.quantity),
            pos.instrument_type,
            float(pos.market_value or 0),
            timestamp
        ))

    conn.commit()
    conn.close()

# --- Main Logic ---
def main():
    print("Logging into Tastytrade...")
    session = Session(
        login=USERNAME,
        password=PASSWORD,
        is_test=not IS_LIVE
    )

    accounts = Account.get(session)

    for acct in accounts:
        balances = acct.get_balances(session)
        positions = acct.get_positions(session)

        print(f"\nAccount: {acct.account_number}")
        print(f"NetLiq: ${balances.net_liquidating_value:,.2f}, Margin: ${balances.margin_equity:,.2f}")

        for pos in positions:
            print(f" - {pos.symbol} x {pos.quantity} [{pos.instrument_type}]")

        save_snapshot(acct, balances, positions)

        # Alert if NetLiq below threshold
        if balances.net_liquidating_value < 1000001:
            send_email(
                subject="⚠️ NetLiq Alert",
                body=f"Account {acct.account_number} NetLiq dropped to ${balances.net_liquidating_value:,.2f}"
            )


if __name__ == "__main__":
    init_db()
    main()
