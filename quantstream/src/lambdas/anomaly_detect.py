
import os, json, decimal, math
import boto3
from boto3.dynamodb.conditions import Key

WINDOW = 20

def lambda_handler(event, context):
    alerts_table = os.getenv("ALERTS_TABLE")
    z_threshold = float(os.getenv("Z_THRESHOLD", "3.0"))

    ddb = boto3.resource("dynamodb")
    prices = ddb.Table(os.getenv("PRICES_TABLE", "PricesTable"))  # optional if wired differently
    alerts = ddb.Table(alerts_table)

    # naive per-record scan (optimize with streams in prod)
    for rec in event.get("Records", []):
        # Expect same Kinesis payload as normalize or hook this to DDB stream
        payload = json.loads(rec.get("body", "{}")) if "body" in rec else {}
        asset = payload.get("asset")
        if not asset:
            continue

        # read last WINDOW rows
        resp = prices.query(
            KeyConditionExpression=Key("pk").eq(f"ASSET#{asset}"),
            ScanIndexForward=False,
            Limit=WINDOW
        )
        items = resp.get("Items", [])
        series = [float(i["price"]) for i in items][::-1]
        if len(series) < 5:
            continue

        mean = sum(series) / len(series)
        var = sum((x - mean)**2 for x in series) / max(1, len(series) - 1)
        std = math.sqrt(var)
        z = 0.0 if std == 0 else (series[-1] - mean) / std

        if abs(z) > z_threshold:
            ts = int(items[-1]["ts"])
            alerts.put_item(Item={
                "asset": asset,
                "ts": ts,
                "z": decimal.Decimal(str(z)),
                "price": decimal.Decimal(str(series[-1])),
                "mean": decimal.Decimal(str(mean)),
                "std": decimal.Decimal(str(std)),
                "message": f"Anomaly for {asset}: z={z:.2f}"
            })

    return {"ok": True}
