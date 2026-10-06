CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    merchant_id TEXT NOT NULL,
    merchant_category TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    device_id TEXT NOT NULL,
    channel TEXT NOT NULL,
    card_present BOOLEAN NOT NULL,
    transaction_ts TIMESTAMPTZ NOT NULL,
    event_ingested_ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_fraud_label BOOLEAN NOT NULL,
    fraud_score NUMERIC(6, 4) NOT NULL,
    fraud_reason TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    transaction_id TEXT NOT NULL REFERENCES transactions(transaction_id),
    customer_id TEXT NOT NULL,
    fraud_score NUMERIC(6, 4) NOT NULL,
    fraud_reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS data_quality_checks (
    check_id BIGSERIAL PRIMARY KEY,
    check_name TEXT NOT NULL,
    check_status TEXT NOT NULL,
    details TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_runs (
    run_id BIGSERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    training_rows INTEGER NOT NULL,
    metrics JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_ts ON transactions(transaction_ts DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_score ON transactions(fraud_score DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_created ON fraud_alerts(created_at DESC);

