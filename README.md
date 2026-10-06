# FinGuard: Real-Time Fraud Intelligence Platform

End-to-end data engineering and AI platform for real-time credit card fraud detection.

FinGuard simulates real-time card transactions, streams them through Kafka-compatible Redpanda, scores fraud risk, stores transactions in PostgreSQL, caches recent alerts in Redis, exposes a FastAPI service, and provides a Streamlit dashboard for live monitoring.

## Why This Project Matters

This is built like a real data engineering system, not just a notebook:

- Real-time ingestion with Kafka-compatible streaming
- Python producer and consumer services
- PostgreSQL data model for transactions, alerts, model runs, and data quality checks
- Redis cache for recent high-risk alerts
- Fraud scoring with feature engineering and rule/ML-ready model structure
- FastAPI service for transactions, alerts, metrics, and scoring
- Streamlit dashboard for live monitoring
- Docker Compose setup for local production-style execution

## Architecture

```text
Synthetic Transaction Generator
        |
        v
Redpanda / Kafka Topic: transactions
        |
        v
Fraud Consumer + Feature Engineering + Scoring
        |
        +--> PostgreSQL: transactions, alerts, quality checks
        |
        +--> Redis: latest fraud alerts
        |
        v
FastAPI API
        |
        v
Streamlit Dashboard
```

## Tech Stack

- Python
- Kafka-compatible streaming with Redpanda
- PostgreSQL
- Redis
- FastAPI
- Streamlit
- Pandas
- Scikit-learn-ready scoring layer
- Docker / Docker Compose
- Pytest

## Quick Start

### Local Demo Without Docker

If Docker is not installed yet, run this simple demo first:

```bash
python3 demo_local.py
```

It creates:

```text
sample_output/fraud_demo_transactions.csv
sample_output/fraud_demo_report.html
```

Open the HTML report in your browser to see generated transactions and fraud scores.

### Full Streaming System With Docker

1. Copy the environment file:

```bash
cp .env.example .env
```

2. Start the platform:

```bash
docker compose up --build
```

3. Open the API:

```text
http://localhost:8000/docs
```

4. Open the dashboard:

```text
http://localhost:8501
```

## Run Services Manually

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run producer:

```bash
python -m src.producer
```

Run consumer:

```bash
python -m src.consumer
```

Run API:

```bash
uvicorn src.api:app --reload --port 8000
```

Run dashboard:

```bash
streamlit run dashboard/app.py
```

## Main Features

### Transaction Streaming

The producer generates realistic card transaction events with:

- customer ID
- merchant
- category
- amount
- location
- device ID
- transaction timestamp
- card-present / online flag
- synthetic fraud label

### Fraud Scoring

The scoring layer combines practical fraud signals:

- unusually high amount
- risky merchant category
- online transaction risk
- unusual country
- night-time transaction
- repeated customer activity
- generated fraud probability

### Storage

PostgreSQL stores:

- all transactions
- fraud alerts
- data quality checks
- model/scoring runs

Redis stores:

- latest high-risk fraud alerts
- lightweight live dashboard data

### API Endpoints

- `GET /health`
- `GET /transactions`
- `GET /alerts`
- `GET /metrics`
- `POST /score`

## Resume Bullets

- Built a real-time fraud detection data platform using Kafka-compatible Redpanda, Python, PostgreSQL, Redis, FastAPI, and Streamlit to process and monitor simulated credit card transactions.
- Designed a streaming pipeline that ingests transaction events, applies feature engineering and fraud scoring, stores results in PostgreSQL, and exposes alerts through API and dashboard layers.
- Implemented fraud-risk features including transaction amount outliers, risky merchant categories, online transaction flags, location risk, and time-based behavior signals.
- Created a production-style Docker Compose environment with separate producer, consumer, API, dashboard, PostgreSQL, Redis, and Redpanda services.

## Interview Explanation

"I built a real-time fraud detection data platform. The system generates synthetic card transactions, streams them through Kafka-compatible Redpanda, consumes them with a Python service, engineers fraud-related features, scores each transaction, stores results in PostgreSQL, caches recent alerts in Redis, and displays metrics through a FastAPI API and Streamlit dashboard. The goal was to show the full data engineering flow from raw event ingestion to reliable storage, real-time scoring, alerting, and analytics."

## Project Structure

```text
finguard-fraud-intelligence-platform/
  dashboard/
  docs/
  infra/
  sql/
  src/
  tests/
  docker-compose.yml
  Dockerfile
  Makefile
  requirements.txt
```
