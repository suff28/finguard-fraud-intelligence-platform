from src.features import build_features


def test_build_features_flags_high_risk_transaction():
    transaction = {
        "amount": 2000,
        "merchant_category": "crypto",
        "country": "NG",
        "channel": "online",
        "card_present": False,
        "transaction_ts": "2026-10-06T02:30:00+00:00",
    }

    features = build_features(transaction)

    assert features["is_high_amount"] is True
    assert features["is_very_high_amount"] is True
    assert features["is_risky_category"] is True
    assert features["is_high_risk_country"] is True
    assert features["is_night_transaction"] is True

