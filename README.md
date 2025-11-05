# ⚡ QuantStream — Real-Time Cloud Pipeline for Market Signals

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Data](https://img.shields.io/badge/Data-Streaming-lightgrey)
![Quant](https://img.shields.io/badge/Quant-Finance-green)
![AI](https://img.shields.io/badge/AI-AnomalyDetection-yellow)

**QuantStream** is a cloud-native, serverless data pipeline for streaming **crypto and equity market signals** in real time.  
It demonstrates a **full end-to-end event-driven architecture** using **AWS Lambda, Kinesis, and DynamoDB**, combined with lightweight **ML-based anomaly detection** to flag liquidity shocks and arbitrage windows.

> Designed for AI, quant, and fintech engineers exploring scalable cloud analytics architectures.

---

## 🧠 Overview

QuantStream continuously ingests live market prices (via CoinGecko API), pushes data to an event stream, normalizes it, and performs rolling z-score analysis for anomaly detection.  
It can be run entirely **locally** (no AWS setup needed) or deployed using the **AWS SAM** reference template.

---

## 🗂 Project Structure

quantstream/
├─ src/
│ ├─ lambdas/
│ │ ├─ ingest_coingecko.py # Fetches live prices and publishes to stream
│ │ ├─ enrich_normalize.py # Normalizes incoming records and writes to DDB
│ │ └─ anomaly_detect.py # Detects statistical outliers (z-scores)
│ └─ shared/utils.py # Common helper functions
├─ infra/
│ └─ template.yaml # AWS SAM template (Kinesis, DDB, Lambda, EventBridge)
├─ local/
│ ├─ run_local.py # Run full simulation locally (no AWS)
│ └─ sample_config.yaml # Example config for assets and intervals
├─ tests/
│ └─ test_anomaly.py # Simple test for anomaly logic
├─ data/.gitkeep
├─ artifacts/.gitkeep
├─ .env.example
├─ requirements.txt
├─ .gitignore
├─ LICENSE
└─ README.md

yaml
Copy code

---

## 🚀 Features

✅ **Real-Time Streaming** — Ingests live crypto prices using CoinGecko  
✅ **Serverless Design** — Event-driven AWS Lambda, Kinesis, DynamoDB pipeline  
✅ **ML-Based Anomaly Detection** — Rolling z-score for liquidity anomalies  
✅ **Local Mode** — Run full simulation offline without AWS  
✅ **Scalable Architecture** — Easily extendable to Uniswap or Binance APIs  

---

## ⚙️ Local Quickstart (No AWS Required)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python local/run_local.py --config local/sample_config.yaml --cycles 5
What happens:

Fetches live BTC/ETH prices from CoinGecko

Computes rolling averages and z-scores

Writes streaming data to /artifacts/prices.csv and /artifacts/alerts.csv

Prints anomaly alerts directly to the terminal

Stop anytime with Ctrl + C.

☁️ AWS Cloud Deployment (Optional Demo)
The included AWS SAM template provisions:

Kinesis Stream for market data ingestion

DynamoDB Tables (PricesTable, AlertsTable)

EventBridge Rule to trigger ingestion Lambda on schedule

Three Lambda Functions (ingest → normalize → anomaly detect)

To deploy:

bash
Copy code
sam build
sam deploy --guided
Note: You’ll need AWS CLI and appropriate IAM permissions.

🧪 Anomaly Detection Logic
QuantStream uses a rolling z-score method to flag anomalies:

ini
Copy code
z = (latest_price - mean) / std
If |z| > threshold, the system logs and alerts the event.
This mimics a volatility detector — ideal for spotting spikes in market liquidity or flash crashes.

You can replace the logic with your own model (e.g., Isolation Forest, Prophet, or LSTM).

🧩 Configuration
Edit .env or local/sample_config.yaml to change assets and parameters:

yaml
Copy code
assets: ["bitcoin", "ethereum"]
base_currency: "usd"
interval_seconds: 15
anomaly_z: 3.0
cycles: 10
🧠 Tech Stack
Python 3.10+ — core language

AWS Lambda / Kinesis / DynamoDB / EventBridge — cloud backbone

AWS SAM — deployment framework

CoinGecko API — market data feed

Pandas / NumPy — statistics & data analysis

💡 Use Cases
Quantitative finance simulations

DeFi / crypto anomaly detection

Market data ingestion architecture demo

ML monitoring pipelines for real-time signals

🪞 Example Output
csharp
Copy code
[ALERT] bitcoin z=3.27 price=47295.0
[ALERT] ethereum z=-3.05 price=1802.2
All prices and alerts are saved under /artifacts/ for later review or visualization.

🧭 Future Enhancements
Integrate Binance & Uniswap APIs for cross-market data

Add AWS S3 historical archiving and Athena queries

Extend anomaly detection with LSTM-based volatility prediction

Real-time dashboard (Streamlit or Grafana Cloud)

📝 License
MIT License © 2025 Rhonda Melo
Use freely for educational or demonstration purposes.

👩‍💻 Author
Rhonda Melo / MelOrchid
🌐 LinkedIn
🎨 #10000HourProject
💬 Pioneering generative AI and quant systems for finance and art.

#AWS #Quant #AI #DeFi #Serverless #CloudArchitecture #Python #BlockchainData
