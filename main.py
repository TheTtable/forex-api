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
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.csv"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Fout bij ophalen CSV: {str(e)}"}), 500

    lines = response.text.splitlines()
    reader = csv.DictReader(lines)

    today = datetime.utcnow().date()
    results = []

    for row in reader:
        try:
            event_date = datetime.strptime(row["Date"].strip(), "%b %d, %Y").date()
            if event_date != today:
                continue

            impact = row["Impact"].strip()
            currency = row["Currency"].strip()
            title = row["Event"].strip()
            time = row["Time"].strip()

            if impact == "High" and currency in ["USD", "EUR"]:
                results.append({
                    "currency": currency,
                    "title": title,
                    "time": time
                })

        except Exception as e:
            # Fout in individuele rij, ga verder met volgende
            print(f"Error parsing row: {e}")
            continue

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
