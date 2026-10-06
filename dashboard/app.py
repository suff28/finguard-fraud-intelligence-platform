import os
import requests
import pandas as pd
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("Real-Time Fraud Detection Dashboard")
st.caption("Streaming transactions, fraud scoring, PostgreSQL storage, Redis alert cache, and FastAPI metrics.")


def get_json(path: str):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=5)
    response.raise_for_status()
    return response.json()


try:
    metrics = get_json("/metrics")
    alerts = get_json("/alerts?limit=25")
    transactions = get_json("/transactions?limit=100")
except Exception as exc:
    st.error(f"Could not reach API: {exc}")
    st.stop()

left, middle, right, fourth = st.columns(4)
left.metric("Transactions", metrics.get("total_transactions", 0))
middle.metric("Avg Fraud Score", metrics.get("avg_fraud_score", 0))
right.metric("High-Risk Transactions", metrics.get("high_risk_transactions", 0))
fourth.metric("Synthetic Fraud Labels", metrics.get("synthetic_fraud_labels", 0))

st.subheader("Latest Fraud Alerts")
if alerts:
    st.dataframe(pd.DataFrame(alerts), use_container_width=True)
else:
    st.info("No alerts yet. Let the producer and consumer run for a minute.")

st.subheader("Recent Transactions")
if transactions:
    df = pd.DataFrame(transactions)
    st.dataframe(df, use_container_width=True)

    st.subheader("Fraud Score by Merchant Category")
    chart_df = df.groupby("merchant_category", as_index=False)["fraud_score"].mean()
    st.bar_chart(chart_df, x="merchant_category", y="fraud_score")
else:
    st.info("No transactions yet.")
