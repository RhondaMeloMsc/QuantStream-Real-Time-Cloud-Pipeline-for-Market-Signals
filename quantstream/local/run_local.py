
import os, csv, time, argparse, yaml, math
from dotenv import load_dotenv
from pathlib import Path
from statistics import mean, pstdev
from typing import List, Dict
import requests

def fetch_prices(assets: List[str], base_currency: str) -> Dict[str, float]:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(assets), "vs_currencies": base_currency}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    return {a: float(data.get(a, {}).get(base_currency)) for a in assets if data.get(a, {}).get(base_currency) is not None}

def zscore(series: List[float]) -> float:
    if len(series) < 5:
        return 0.0
    m = mean(series)
    # population std for simplicity in streaming demo
    s = pstdev(series) if len(series) > 1 else 0.0
    return 0.0 if s == 0 else (series[-1] - m) / s

def main():
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="local/sample_config.yaml")
    ap.add_argument("--cycles", type=int, default=0, help="Override cycles (0 = from config)")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, "r"))
    assets = cfg.get("assets", ["bitcoin","ethereum"])
    base = cfg.get("base_currency", "usd")
    interval = int(cfg.get("interval_seconds", 10))
    thresh = float(cfg.get("anomaly_z", 3.0))
    cycles = int(args.cycles or cfg.get("cycles", 5))

    artifacts = Path("artifacts")
    artifacts.mkdir(parents=True, exist_ok=True)
    price_path = artifacts / "prices.csv"
    alert_path = artifacts / "alerts.csv"

    # init files
    if not price_path.exists():
        with open(price_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ts","asset","price"])
    if not alert_path.exists():
        with open(alert_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ts","asset","price","z","mean","std"])

    history = {a: [] for a in assets}
    count = 0
    while True:
        ts = int(time.time())
        prices = fetch_prices(assets, base)
        with open(price_path, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for a, p in prices.items():
                w.writerow([ts, a, p])
                history[a].append(p)
                if len(history[a]) > 50:
                    history[a] = history[a][-50:]
                z = zscore(history[a])
                if abs(z) > thresh:
                    m = mean(history[a])
                    s = pstdev(history[a]) if len(history[a]) > 1 else 0.0
                    with open(alert_path, "a", newline="", encoding="utf-8") as fa:
                        wa = csv.writer(fa)
                        wa.writerow([ts, a, p, round(z,3), round(m,3), round(s,3)])
                    print(f"[ALERT] {a} z={z:.2f} price={p}")
        count += 1
        if cycles and count >= cycles:
            break
        time.sleep(interval)

if __name__ == "__main__":
    main()
