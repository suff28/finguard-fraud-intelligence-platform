from pathlib import Path
import csv
from html import escape

from src.generator import generate_transaction
from src.fraud_model import score_transaction


def main() -> None:
    output_dir = Path("sample_output")
    output_dir.mkdir(exist_ok=True)

    rows = []
    for _ in range(100):
        transaction = generate_transaction()
        score = score_transaction(transaction)
        rows.append(
            {
                **transaction,
                "fraud_score": score["fraud_score"],
                "fraud_reason": score["fraud_reason"],
            }
        )

    csv_path = output_dir / "fraud_demo_transactions.csv"
    html_path = output_dir / "fraud_demo_report.html"

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    high_risk = [row for row in rows if row["fraud_score"] >= 0.72]
    avg_score = sum(float(row["fraud_score"]) for row in rows) / len(rows)

    html = [
        "<html><head><title>Fraud Detection Demo</title>",
        "<style>body{font-family:Arial;margin:32px;} table{border-collapse:collapse;width:100%;} th,td{border:1px solid #ddd;padding:8px;font-size:13px;} th{background:#111;color:white;} .risk{color:#b00020;font-weight:bold;} .metric{display:inline-block;margin-right:24px;padding:12px;border:1px solid #ddd;border-radius:6px;}</style>",
        "</head><body>",
        "<h1>Fraud Detection Demo Report</h1>",
        "<p>This local demo generated 100 synthetic card transactions and scored fraud risk using the project scoring logic.</p>",
        f"<div class='metric'><b>Total Transactions</b><br>{len(rows)}</div>",
        f"<div class='metric'><b>High-Risk Alerts</b><br>{len(high_risk)}</div>",
        f"<div class='metric'><b>Average Fraud Score</b><br>{avg_score:.4f}</div>",
        "<h2>Top High-Risk Transactions</h2>",
        "<table><tr><th>Transaction ID</th><th>Customer</th><th>Amount</th><th>Country</th><th>Category</th><th>Score</th><th>Reason</th></tr>",
    ]

    for row in sorted(rows, key=lambda item: item["fraud_score"], reverse=True)[:15]:
        risk_class = "risk" if row["fraud_score"] >= 0.72 else ""
        html.append(
            "<tr>"
            f"<td>{escape(row['transaction_id'])}</td>"
            f"<td>{escape(row['customer_id'])}</td>"
            f"<td>${float(row['amount']):,.2f}</td>"
            f"<td>{escape(row['country'])}</td>"
            f"<td>{escape(row['merchant_category'])}</td>"
            f"<td class='{risk_class}'>{row['fraud_score']}</td>"
            f"<td>{escape(row['fraud_reason'])}</td>"
            "</tr>"
        )

    html.extend(["</table>", "</body></html>"])
    html_path.write_text("\n".join(html))

    print(f"Wrote {csv_path}")
    print(f"Wrote {html_path}")
    print(f"High-risk alerts: {len(high_risk)}")


if __name__ == "__main__":
    main()

