from src.features import build_features


def score_transaction(transaction: dict) -> dict:
    features = build_features(transaction)

    score = 0.05
    reasons = []

    if features["is_high_amount"]:
        score += 0.18
        reasons.append("high amount")
    if features["is_very_high_amount"]:
        score += 0.20
        reasons.append("very high amount")
    if features["is_risky_category"]:
        score += 0.16
        reasons.append("risky merchant category")
    if features["is_high_risk_country"]:
        score += 0.22
        reasons.append("high-risk country")
    if features["is_online"]:
        score += 0.08
        reasons.append("online transaction")
    if features["is_card_not_present"]:
        score += 0.08
        reasons.append("card not present")
    if features["is_night_transaction"]:
        score += 0.10
        reasons.append("night transaction")

    if transaction.get("device_id", "").endswith("999"):
        score += 0.15
        reasons.append("suspicious device pattern")

    fraud_score = min(round(score, 4), 0.99)

    return {
        "fraud_score": fraud_score,
        "fraud_reason": ", ".join(reasons) if reasons else "low-risk transaction",
        "features": features,
    }

