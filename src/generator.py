import random
import uuid
from datetime import datetime, timezone


MERCHANT_CATEGORIES = [
    "grocery",
    "gas",
    "restaurant",
    "retail",
    "travel",
    "electronics",
    "crypto",
    "gift_cards",
]

COUNTRIES = ["US", "US", "US", "US", "CA", "GB", "IN", "NG", "RU"]
CITIES = {
    "US": ["Boston", "New York", "Chicago", "San Francisco", "Austin"],
    "CA": ["Toronto", "Vancouver"],
    "GB": ["London", "Manchester"],
    "IN": ["Bengaluru", "Mumbai"],
    "NG": ["Lagos"],
    "RU": ["Moscow"],
}


def generate_transaction() -> dict:
    country = random.choice(COUNTRIES)
    category = random.choice(MERCHANT_CATEGORIES)
    risky = category in {"crypto", "gift_cards", "electronics"} or country in {"NG", "RU"}

    if risky and random.random() < 0.45:
        amount = round(random.uniform(700, 3500), 2)
    else:
        amount = round(random.lognormvariate(3.6, 0.8), 2)

    channel = random.choice(["online", "mobile", "in_store"])
    card_present = channel == "in_store"
    is_fraud = risky and amount > 600 and channel != "in_store" and random.random() < 0.65

    device_suffix = "999" if is_fraud and random.random() < 0.35 else str(random.randint(100, 998))

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST-{random.randint(1000, 1150)}",
        "merchant_id": f"MERCH-{random.randint(200, 260)}",
        "merchant_category": category,
        "amount": amount,
        "currency": "USD",
        "country": country,
        "city": random.choice(CITIES[country]),
        "device_id": f"DEV-{random.randint(10, 99)}-{device_suffix}",
        "channel": channel,
        "card_present": card_present,
        "transaction_ts": datetime.now(timezone.utc).isoformat(),
        "is_fraud_label": is_fraud,
    }

