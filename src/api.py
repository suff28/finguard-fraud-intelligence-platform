import json
from fastapi import FastAPI, Query
from pydantic import BaseModel
import redis
from sqlalchemy import text

from src.config import get_settings
from src.db import db_session
from src.fraud_model import score_transaction


app = FastAPI(title="Real-Time Fraud Detection API")


class TransactionRequest(BaseModel):
    transaction_id: str
    customer_id: str
    merchant_id: str
    merchant_category: str
    amount: float
    currency: str = "USD"
    country: str
    city: str
    device_id: str
    channel: str
    card_present: bool
    transaction_ts: str
    is_fraud_label: bool = False


def get_redis_client():
    settings = get_settings()
    return redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(transaction: TransactionRequest):
    return score_transaction(transaction.model_dump())


@app.get("/transactions")
def transactions(limit: int = Query(default=50, ge=1, le=500)):
    query = text(
        """
        SELECT transaction_id, customer_id, merchant_category, amount, country,
               city, channel, card_present, transaction_ts, fraud_score, fraud_reason
        FROM transactions
        ORDER BY transaction_ts DESC
        LIMIT :limit
        """
    )
    with db_session() as connection:
        rows = connection.execute(query, {"limit": limit}).mappings().all()
    return [dict(row) for row in rows]


@app.get("/alerts")
def alerts(limit: int = Query(default=25, ge=1, le=100)):
    query = text(
        """
        SELECT alert_id, transaction_id, customer_id, fraud_score, fraud_reason, created_at
        FROM fraud_alerts
        ORDER BY created_at DESC
        LIMIT :limit
        """
    )
    with db_session() as connection:
        rows = connection.execute(query, {"limit": limit}).mappings().all()
    return [dict(row) for row in rows]


@app.get("/alerts/recent-cache")
def recent_cached_alerts():
    redis_client = get_redis_client()
    values = redis_client.lrange("fraud_alerts", 0, 20)
    return [json.loads(value) for value in values]


@app.get("/metrics")
def metrics():
    query = text(
        """
        SELECT
            COUNT(*) AS total_transactions,
            COALESCE(ROUND(AVG(fraud_score), 4), 0) AS avg_fraud_score,
            COUNT(*) FILTER (WHERE fraud_score >= 0.72) AS high_risk_transactions,
            COUNT(*) FILTER (WHERE is_fraud_label = true) AS synthetic_fraud_labels
        FROM transactions
        """
    )
    with db_session() as connection:
        row = connection.execute(query).mappings().one()
    return dict(row)

