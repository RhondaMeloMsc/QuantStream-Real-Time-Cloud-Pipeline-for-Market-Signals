
import os, json, base64
import boto3  # available in AWS Lambda runtime
from ..shared.utils import get_assets_env, fetch_prices, now_ts

def lambda_handler(event, context):
    stream_name = os.getenv("STREAM_NAME")
    base_currency = os.getenv("BASE_CURRENCY", "usd")
    assets = get_assets_env()

    prices = fetch_prices(assets, base_currency)
    ts = now_ts()

    kinesis = boto3.client("kinesis")
    for asset, price in prices.items():
        payload = {"ts": ts, "asset": asset, "price": price, "currency": base_currency}
        kinesis.put_record(StreamName=stream_name, Data=json.dumps(payload).encode("utf-8"), PartitionKey=asset)

    return {"ok": True, "count": len(prices)}
