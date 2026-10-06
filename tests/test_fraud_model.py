from src.fraud_model import score_transaction


def test_score_transaction_returns_high_score_for_risky_event():
    transaction = {
        "transaction_id": "test-1",
        "customer_id": "CUST-1",
        "merchant_id": "MERCH-1",
        "merchant_category": "crypto",
        "amount": 2500,
        "currency": "USD",
        "country": "NG",
        "city": "Lagos",
        "device_id": "DEV-22-999",
        "channel": "online",
        "card_present": False,
        "transaction_ts": "2026-10-06T02:30:00+00:00",
        "is_fraud_label": True,
    }

    score = score_transaction(transaction)

    assert score["fraud_score"] >= 0.72
    assert "high amount" in score["fraud_reason"]

