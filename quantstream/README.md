
# 📡 QuantStream — Real-Time Cloud Pipeline for Market Signals

**Serverless reference architecture** for streaming crypto + equity market data into a cloud pipeline with **ingestion → normalization → anomaly detection → alerts**.  
Designed to demonstrate **AWS cloud architecture** while remaining fully **runnable locally** for demos.

> Tech focus: **AWS Lambda, Kinesis, DynamoDB, EventBridge** (+ local simulation), **Python**, **ML anomaly flags**.

---

## 🌐 What this shows
- **Event-driven design** for market data
- **Cloud resources** (via AWS SAM template) — Kinesis stream, DynamoDB tables, scheduled Lambda
- **ML-lite** anomaly detection (rolling z-score) for liquidity shocks & spikes
- **Local runner** (no AWS needed) to fetch data (CoinGecko), normalize, flag anomalies, and store CSV artifacts

---

## 🗂 Repository layout
```
quantstream/
├─ src/
│  ├─ lambdas/
│  │  ├─ ingest_coingecko.py     # (Lambda) poll CoinGecko → push to stream
│  │  ├─ enrich_normalize.py     # (Lambda) normalize stream payloads
│  │  └─ anomaly_detect.py       # (Lambda) z-score flags → Alerts table
│  └─ shared/
│     └─ utils.py                # common parsing/math
├─ infra/
│  └─ template.yaml              # AWS SAM: Kinesis + DynamoDB + Lambdas + schedule
├─ local/
│  ├─ run_local.py               # Local end-to-end simulation (no AWS required)
│  └─ sample_config.yaml         # Assets, thresholds, intervals
├─ tests/
│  └─ test_anomaly.py            # minimal unit test for z-score logic
├─ data/.gitkeep
├─ artifacts/.gitkeep
├─ requirements.txt
├─ .env.example
├─ .gitignore
├─ LICENSE
└─ README.md
```

---

## 🛠️ Local quickstart (no AWS required)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python local/run_local.py --config local/sample_config.yaml --cycles 5
```

This will:
1. Fetch prices for configured assets
2. Normalize + compute rolling z-scores
3. Write outputs to `artifacts/` (CSV) and print any anomaly alerts

> You can increase `--cycles` to keep streaming locally. Use Ctrl+C to stop.

---

## ☁️ AWS deployment (reference)

The repo includes an **AWS SAM** template (`infra/template.yaml`) wiring:
- **Kinesis**: `MarketStream`
- **DynamoDB**: `PricesTable`, `AlertsTable`
- **EventBridge**: Scheduler for `IngestFunction` (e.g., every minute)
- **Three Lambdas**: Ingest → Normalize → Anomaly

> **Note:** This template is a reference for interviews/architecture reviews. You can deploy with `sam build && sam deploy` after adding your AWS account/region, but the local runner provides a fast, zero-cost demo.

---

## 🧪 Anomaly detection (how it works)
We compute **rolling mean/std** per asset and flag any point where `|z| > threshold`.  
This is intentionally simple; plug in your own model (e.g., Isolation Forest, Prophet) inside `src/lambdas/anomaly_detect.py` or the local runner.

---

## 🔐 Notes
- This is educational demo code — **not** investment advice.
- Keep secrets out of git. Use `.env` only locally.

MIT © 2025 Rhonda Melo
