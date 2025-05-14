import sys
from pathlib import Path

# 🔧 Force local import path for the tastytrade_sdk source
sdk_path = Path(__file__).resolve().parents[2] / "tastytrade-sdk-python" / "src"
sys.path.insert(0, str(sdk_path))

print("Looking in:", sdk_path)

try:
    from tastytrade_sdk.session import Session
    print("✅ SUCCESS: tastytrade_sdk is importable")
except ModuleNotFoundError as e:
    print("❌ FAIL:", e)
