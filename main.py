from flask import Flask, jsonify
import csv
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Forex API werkt ✅"

@app.route("/news")
def get_news():
    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.csv"
    response = requests.get(url)
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)

    today = datetime.utcnow().date()
    results = []

    for row in reader:  # ✅ correct ingesprongen
        try:
            event_date = datetime.strptime(row["Date"].strip(), "%b %d, %Y").date()
            print(row["Date"], row["Currency"], row["Impact"], row["Event"])

            if event_date != today:
                continue

            impact = row["Impact"].strip()
            currency = row["Currency"].strip()
            title = row["Event"].strip()
            time = row["Time"].strip()

            print(f"{event_date} | {impact} | {currency} | {title}")

            if impact == "High" and currency in ["USD", "EUR"]:
                results.append({
                    "currency": currency,
                    "title": title,
                    "time": time
                })
        except Exception as e:
            print(f"Error parsing row: {e}")
            continue

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
