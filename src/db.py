from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True)


@contextmanager
def db_session():
    engine = get_engine()
    with engine.begin() as connection:
        yield connection


def insert_transaction(transaction: dict, score: dict) -> None:
    query = text(
        """
        INSERT INTO transactions (
            transaction_id, customer_id, merchant_id, merchant_category,
            amount, currency, country, city, device_id, channel, card_present,
            transaction_ts, is_fraud_label, fraud_score, fraud_reason
        )
        VALUES (
            :transaction_id, :customer_id, :merchant_id, :merchant_category,
            :amount, :currency, :country, :city, :device_id, :channel, :card_present,
            :transaction_ts, :is_fraud_label, :fraud_score, :fraud_reason
        )
        ON CONFLICT (transaction_id) DO NOTHING
        """
    )
    payload = {**transaction, **score}
    with db_session() as connection:
        connection.execute(query, payload)


def insert_alert(transaction: dict, score: dict) -> None:
    query = text(
        """
        INSERT INTO fraud_alerts (
            transaction_id, customer_id, fraud_score, fraud_reason
        )
        VALUES (
            :transaction_id, :customer_id, :fraud_score, :fraud_reason
        )
        """
    )
    payload = {
        "transaction_id": transaction["transaction_id"],
        "customer_id": transaction["customer_id"],
        "fraud_score": score["fraud_score"],
        "fraud_reason": score["fraud_reason"],
    }
    with db_session() as connection:
        connection.execute(query, payload)


def insert_quality_check(check_name: str, check_status: str, details: str) -> None:
    query = text(
        """
        INSERT INTO data_quality_checks (check_name, check_status, details)
        VALUES (:check_name, :check_status, :details)
        """
    )
    with db_session() as connection:
        connection.execute(
            query,
            {
                "check_name": check_name,
                "check_status": check_status,
                "details": details,
            },
        )

