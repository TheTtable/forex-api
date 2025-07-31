@app.route("/news")
def get_news():
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.csv"
    response = requests.get(url)
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)

    today = datetime.utcnow().date()
    print("✅ Vandaag (UTC):", today)

    results = []

    for row in reader:
        try:
            event_date = datetime.strptime(row["Date"].strip(), "%b %d, %Y").date()

            if event_date == today:
                print(f"🔍 Vandaag gevonden: {row}")

            impact = row["Impact"].strip()
            currency = row["Currency"].strip()
            title = row["Event"].strip()
            time = row["Time"].strip()

            print(f"🧪 {event_date} | {impact} | {currency} | {title}")

            if event_date != today:
                continue

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
