
import os, json, decimal
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    table_name = os.getenv("PRICES_TABLE")
    ddb = boto3.resource("dynamodb").Table(table_name)

    # Kinesis batch of records
    for rec in event.get("Records", []):
        payload = json.loads(rec["kinesis"]["data"], strict=False)
        asset = payload["asset"]
        ts = int(payload["ts"])
        price = float(payload["price"])

        item = {
            "pk": f"ASSET#{asset}",
            "sk": f"TS#{ts}",
            "asset": asset,
            "ts": ts,
            "price": decimal.Decimal(str(price)),
        }
        ddb.put_item(Item=item)

    return {"ok": True, "processed": len(event.get("Records", []))}
