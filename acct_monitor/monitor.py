from tastytrade import User
import acct_monitor.db as db
import datetime

async def fetch_and_store(user):
    conn = db.get_connection()
    cursor = conn.cursor()

    accounts = await user.get_accounts()

    for account in accounts:
        await account.refresh_balances()
        cursor.execute('''
            INSERT OR REPLACE INTO accounts (account, account_type, margin_balance, liquidating_equity, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            account.account_number,
            account.account_type,
            account.margin_balance,
            account.liquidating_equity,
            datetime.datetime.now()
        ))

        positions = await account.get_positions()
        for pos in positions:
            cursor.execute('''
                INSERT INTO positions (account, symbol, quantity, instrument_type, market_value)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                account.account_number,
                pos.symbol,
                pos.quantity,
                pos.instrument_type,
                pos.market_value or 0
            ))

    conn.commit()
    conn.close()
