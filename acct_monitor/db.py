import sqlite3

def get_connection():
    return sqlite3.connect("acct_monitor.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT,
            symbol TEXT,
            quantity REAL,
            instrument_type TEXT,
            market_value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account TEXT PRIMARY KEY,
            account_type TEXT,
            margin_balance REAL,
            liquidating_equity REAL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
