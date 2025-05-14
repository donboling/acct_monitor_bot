import sys
import os
from pathlib import Path

# Force local import of tastytrade_sdk
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "tastytrade-sdk-python" / "src"))

from tastytrade_sdk.session import Session
from tastytrade_sdk.orders import (
    Order, OrderDetails, NewOrder,
    OrderAction, OrderType, TimeInForce
)

# === Load .env ===
load_dotenv()
USERNAME = os.getenv("TT_USERNAME")
PASSWORD = os.getenv("TT_PASSWORD")
IS_LIVE = os.getenv("TT_IS_LIVE", "False").lower() == "true"
ACCOUNT = os.getenv("TT_ACCOUNT")

# === Login ===
session = Session(
    login=USERNAME,
    password=PASSWORD,
    is_test=not IS_LIVE
)

# === Get next Friday's expiration ===
today = datetime.date.today()
days_until_friday = (4 - today.weekday()) % 7
next_friday = today + datetime.timedelta(days=days_until_friday)
exp_str = next_friday.strftime("%m%d%y")  # MMDDYY

# === Define covered call legs ===
stock_leg = OrderDetails(
    action=OrderAction.BUY_TO_OPEN,
    quantity=100,
    instrument_type="Equity",
    symbol="AAPL"
)

call_leg = OrderDetails(
    action=OrderAction.SELL_TO_OPEN,
    quantity=1,
    instrument_type="Option",
    symbol=f"AAPL_{exp_str}C205"
)

# === Create order ===
covered_call = NewOrder(
    type=OrderType.MARKET,
    time_in_force=TimeInForce.DAY,
    legs=[stock_leg, call_leg]
)

# === Submit order ===
try:
    response = Order.place(session, ACCOUNT, covered_call)
    print("✅ Covered call order placed:")
    print(response)
except Exception as e:
    print("❌ Order failed:", str(e))
