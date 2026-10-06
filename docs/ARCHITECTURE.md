# Architecture

## Data Flow

1. `src.producer` creates synthetic credit card transactions.
2. Events are written to the Kafka topic `transactions` on Redpanda.
3. `src.consumer` reads events, validates them, builds fraud features, scores risk, and writes results.
4. PostgreSQL stores transaction history, alerts, data quality checks, and model run metadata.
5. Redis stores the latest high-risk alerts for fast dashboard access.
6. FastAPI exposes health, metrics, transactions, alerts, and scoring endpoints.
7. Streamlit displays live metrics, alerts, transaction tables, and category-level fraud trends.

## Why Redpanda?

Redpanda is Kafka API-compatible and easier to run locally than a full Kafka/Zookeeper setup.

## Why PostgreSQL?

PostgreSQL is a strong transactional database for structured event storage, analytics queries, and indexes.

## Why Redis?

Redis is useful for low-latency access to recent alerts without repeatedly querying the database.

## Production Improvements

- Add Airflow or Dagster orchestration for batch quality checks.
- Replace rule scoring with a trained supervised model.
- Add model monitoring and drift detection.
- Add authentication and role-based API access.
- Add CI/CD with GitHub Actions.
- Deploy API and dashboard to cloud infrastructure.

