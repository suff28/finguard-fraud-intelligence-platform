from datetime import datetime


RISKY_CATEGORIES = {"crypto", "electronics", "gift_cards", "travel"}
HIGH_RISK_COUNTRIES = {"NG", "RU", "KP", "IR"}


def build_features(transaction: dict) -> dict:
    ts = _parse_timestamp(transaction["transaction_ts"])
    amount = float(transaction["amount"])
    category = transaction["merchant_category"]
    country = transaction["country"]
    channel = transaction["channel"]

    return {
        "amount": amount,
        "log_amount": _safe_log_bucket(amount),
        "is_high_amount": amount >= 700,
        "is_very_high_amount": amount >= 1500,
        "is_risky_category": category in RISKY_CATEGORIES,
        "is_high_risk_country": country in HIGH_RISK_COUNTRIES,
        "is_online": channel == "online",
        "is_night_transaction": ts.hour < 5 or ts.hour >= 23,
        "is_card_not_present": not bool(transaction["card_present"]),
    }


def _parse_timestamp(value: str) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _safe_log_bucket(amount: float) -> float:
    if amount <= 0:
        return 0.0
    if amount < 25:
        return 1.0
    if amount < 100:
        return 2.0
    if amount < 500:
        return 3.0
    if amount < 1500:
        return 4.0
    return 5.0

