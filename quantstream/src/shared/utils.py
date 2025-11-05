
import os
import time
from typing import List, Dict
import requests

COINGECKO_SIMPLE_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_assets_env(default: str = "bitcoin,ethereum") -> List[str]:
    raw = os.getenv("ASSETS", default)
    return [a.strip() for a in raw.split(",") if a.strip()]

def fetch_prices(assets: List[str], base_currency: str = "usd") -> Dict[str, float]:
    params = {"ids": ",".join(assets), "vs_currencies": base_currency}
    r = requests.get(COINGECKO_SIMPLE_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    out = {}
    for a in assets:
        price = data.get(a, {}).get(base_currency)
        if price is not None:
            out[a] = float(price)
    return out

def now_ts() -> int:
    return int(time.time())
