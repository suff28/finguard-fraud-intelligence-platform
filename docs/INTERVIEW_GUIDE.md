# Interview Guide

## Short Explanation

"I built a real-time fraud detection data platform. It generates synthetic card transactions, streams them through Kafka-compatible Redpanda, consumes the events with Python, engineers fraud features, scores each transaction, stores results in PostgreSQL, caches recent alerts in Redis, and exposes everything through a FastAPI API and Streamlit dashboard."

## What Problem It Solves

Financial companies need to identify suspicious transactions quickly. This project shows how raw transaction events can move through a real-time data pipeline, get validated, scored, stored, and surfaced to analysts.

## Data Engineering Skills Shown

- Event streaming
- ETL/ELT pipeline design
- Data validation
- PostgreSQL schema design
- Query indexes
- API development
- Dashboarding
- Dockerized services
- Redis caching

## AI / ML Skills Shown

- Feature engineering
- Fraud risk scoring
- Model-ready architecture
- Alert thresholding
- Model monitoring-ready structure

## Strong Interview Answer

"The hardest part was designing it as a full system instead of only a model. A fraud model is useful only if transactions can be ingested reliably, validated, scored quickly, stored correctly, and displayed to users. So I built the project around the full lifecycle: producer, streaming topic, consumer, fraud scoring, PostgreSQL storage, Redis alert cache, API, and dashboard."

