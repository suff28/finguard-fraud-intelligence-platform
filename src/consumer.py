import json
import signal
from confluent_kafka import Consumer
import redis

from src.config import get_settings
from src.db import insert_alert, insert_quality_check, insert_transaction
from src.fraud_model import score_transaction


running = True


def stop_handler(signum, frame) -> None:
    global running
    running = False


def validate_event(event: dict) -> tuple[bool, str]:
    required = [
        "transaction_id",
        "customer_id",
        "merchant_id",
        "merchant_category",
        "amount",
        "currency",
        "country",
        "city",
        "device_id",
        "channel",
        "card_present",
        "transaction_ts",
        "is_fraud_label",
    ]
    missing = [field for field in required if field not in event]
    if missing:
        return False, f"missing fields: {missing}"
    if float(event["amount"]) < 0:
        return False, "amount cannot be negative"
    return True, "valid"


def main() -> None:
    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    settings = get_settings()
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": settings.kafka_group_id,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([settings.kafka_topic])

    redis_client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )

    print(f"Consuming from topic={settings.kafka_topic}")
    try:
        while running:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            event = json.loads(message.value().decode("utf-8"))
            is_valid, details = validate_event(event)
            if not is_valid:
                insert_quality_check("transaction_event_validation", "failed", details)
                continue

            score = score_transaction(event)
            insert_transaction(event, score)

            if score["fraud_score"] >= settings.fraud_alert_threshold:
                insert_alert(event, score)
                redis_client.lpush(
                    "fraud_alerts",
                    json.dumps(
                        {
                            "transaction_id": event["transaction_id"],
                            "customer_id": event["customer_id"],
                            "amount": event["amount"],
                            "country": event["country"],
                            "fraud_score": score["fraud_score"],
                            "fraud_reason": score["fraud_reason"],
                            "transaction_ts": event["transaction_ts"],
                        }
                    ),
                )
                redis_client.ltrim("fraud_alerts", 0, 49)

            print(
                f"transaction={event['transaction_id']} "
                f"score={score['fraud_score']} reason={score['fraud_reason']}"
            )
    finally:
        consumer.close()


if __name__ == "__main__":
    main()

