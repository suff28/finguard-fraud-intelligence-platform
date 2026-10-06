import json
import time
from confluent_kafka import Producer

from src.config import get_settings
from src.generator import generate_transaction


def delivery_report(error, message) -> None:
    if error:
        print(f"Delivery failed: {error}")
    else:
        print(f"Produced event to {message.topic()}[{message.partition()}]")


def main() -> None:
    settings = get_settings()
    producer = Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})

    print(f"Producing transactions to topic={settings.kafka_topic}")
    while True:
        event = generate_transaction()
        producer.produce(
            settings.kafka_topic,
            key=event["transaction_id"],
            value=json.dumps(event),
            callback=delivery_report,
        )
        producer.poll(0)
        time.sleep(settings.producer_sleep_seconds)


if __name__ == "__main__":
    main()

