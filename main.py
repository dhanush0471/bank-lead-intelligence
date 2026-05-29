import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# TEST DATA (since MCA API access is restricted publicly)
companies = [
    {"name": "ABC Technologies Pvt Ltd", "city": "Bangalore", "state": "Karnataka"},
    {"name": "XYZ Finance Pvt Ltd", "city": "Mysore", "state": "Karnataka"},
    {"name": "Random Traders", "city": "Mumbai", "state": "Maharashtra"}
]

for c in companies:

    score = 0

    if c["state"] == "Karnataka":
        score += 40

    if "Bangalore" in c["city"]:
        score += 30

    if "Pvt" in c["name"]:
        score += 20

    if score >= 60:
        msg = f"""
🏦 NEW BANK LEAD

🏢 {c['name']}
📍 {c['city']}, {c['state']}

⭐ Score: {score}/100
⏱ {datetime.now()}
"""
        send(msg)

send("✅ CRM RUN COMPLETED")
